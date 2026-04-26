import json
import logging
import typing as t
import uuid

from google.adk.agents import (
    Agent,
    BaseAgent,
    LoopAgent,
    ParallelAgent,
    SequentialAgent,
)
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.models.google_llm import Gemini
from google.genai import types
from pydantic import BaseModel, Field

from ...tools.rag import ExperienceRetrieval, ValidExperienceKeys


class KeywordsOutputSchema(BaseModel):
    keywords: list[str] = Field(
        ...,
        description="List of relevant keywords or skills.",
    )


class SummaryKeywordsOutputSchema(KeywordsOutputSchema):
    summary: str = Field(
        ...,
        description="A brief summary of the experience.",
    )


class SummaryHighlightsKeywordsOutputSchema(SummaryKeywordsOutputSchema):
    highlights: list[str] = Field(
        ...,
        description="Key achievements or highlights of the experience.",
    )


OUTPUT_SCHEMAS = {
    "work": SummaryHighlightsKeywordsOutputSchema,
    "volunteer": SummaryHighlightsKeywordsOutputSchema,
    "certificates": SummaryKeywordsOutputSchema,
    "projects": SummaryHighlightsKeywordsOutputSchema,
    "skills": KeywordsOutputSchema,
    "interests": KeywordsOutputSchema,
}


EXAMPLES = {
    "work": {
        "summary": "Description…",
        "highlights": ["Started the company"],
        "keywords": ["leadership", "entrepreneurship"],
    },
    "volunteer": {
        "summary": "Description…",
        "highlights": ["Volunteered at local shelter"],
        "keywords": ["community", "helping others"],
    },
    "certificates": {
        "summary": "Description…",
        "keywords": ["certification", "achievement"],
    },
    "projects": {
        "summary": "Description…",
        "highlights": ["Developed a web app"],
        "keywords": ["Python", "Django", "AWS"],
    },
    "skills": {
        "keywords": ["Python", "Machine Learning", "Data Analysis"],
    },
    "interests": {
        "keywords": ["hiking", "photography", "travel"],
    },
}


PROMPT_INITIAL_EXP_ENHANCEMENT = """
You are an experience enhancer. Your task is to improve the provided
description of experience to better align it with the job posting summary.

The main goal is to ensure that the experience description highlights
the skills, technologies, and accomplishments that are most relevant to
the job requirements and technology stack mentioned in the job posting.

Job Posting Summary:
{{summarized_job_offer}}

Experience Description:
{{experience_{agent_id}}}

EXAMPLE:
{example}

YOU MUST RETURN the output in the EXACT FORMAT as shown in the example,
without any additional text. NOT FOLLOWING THE FORMAT WILL CAUSE ERRORS.

OUTPUT RULES:
- The summary/description must be concise and focused on relevant skills
    and accomplishments. Avoid unnecessary details. Try to keep it
    in 1-2 sentences.
- The highlights must be specific achievements or contributions,
    quantifiable where possible. Try to include 2-3 highlights. Each highlight
    should start with a strong action verb. Try to keep it in a sentence each.
- The keywords must include relevant technologies, tools, and skills.
    Try to include 3-5 keywords.
- Do not invent details. Only use the information provided in the
    experience description.
- Mantain the original language of the experience description.
"""

PROMPT_CRITIC = """
You are a constructive critic. Your task is to review the provided
draft of experience and provide feedback on how well it aligns with the
job posting summary. Identify areas of improvement, suggest enhancements,
and highlight any discrepancies between the draft and the job requirements.

Job Posting Summary:
{{summarized_job_offer}}

Experience Draft:
{{enhanced_experience_{agent_id}}}

- If the draft is well-aligned, you MUST respond with the exact phrase: 'APPROVED'
- Otherwise, provide 1-3 specific, actionable suggestions for improvement,
    of the draft to better align it with the job posting summary.
- Be concise and specific in your feedback. Think about your suggestions
    will be used for other agent to improve the experience draft.
"""

PROMPT_REFINER_EXP_ENHANCEMENT = """
You are an experience enhancer. Your task is to improve the provided
description of experience to better align it with the job posting summary.
The main goal is to ensure that the experience description highlights
the skills, technologies, and accomplishments that are most relevant to
the job requirements and technology stack mentioned in the job posting.

Job Posting Summary:
{{summarized_job_offer}}

Original Experience Description:
{{experience_{agent_id}}}

Current Experience Draft:
{{enhanced_experience_{agent_id}}}

Critique Feedback:
{{critique_{agent_id}}}

EXAMPLE:
{example}

YOU MUST RETURN the output in the EXACT FORMAT as shown in the example,
without any additional text. NOT FOLLOWING THE FORMAT WILL CAUSE ERRORS.

OUTPUT RULES:
- Use the critique feedback to make specific improvements
    to the experience draft to better align it with the job posting summary.
- The summary/description must be concise and focused on relevant skills
    and accomplishments. Avoid unnecessary details. Try to keep it
    in 1-2 sentences.
- The highlights must be specific achievements or contributions,
    quantifiable where possible. Try to include 2-3 highlights. Each highlight
    should start with a strong action verb. Try to keep it in a sentence each.
- The keywords must include relevant technologies, tools, and skills.
    Try to include 3-5 keywords.
- Do not invent details. Only use the information provided in the
    experience description.
- Mantain the original language of the experience description.
"""


retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    initial_delay=1,
    max_delay=60,  # Maximum delay between retries
    exp_base=3,  # Delay multiplier
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

experience_refiner_model = Gemini(
    model="gemini-2.5-flash-preview-09-2025",
    retry_options=retry_config,
)

experience_critique_model = Gemini(
    model="gemini-2.5-pro",
    retry_options=retry_config,
)

MAX_REFINEMENT_ITERATIONS = 1


class CheckStatusAndEscalateAgent(BaseAgent):
    """An agent that checks the status of the experience refinement
    and escalates if approved."""

    agent_id: str

    @t.override
    async def _run_async_impl(self, ctx: InvocationContext) -> t.AsyncGenerator[Event]:
        logging.info(f"[{self.name}] Starting Check Status And Escalate Agent")

        # Get the critique result from the session state
        critique_result = ctx.session.state.get(f"critique_{self.agent_id}", "fail")
        should_stop = critique_result.lower() == "approved"

        logging.debug(
            f"[{self.name}] Critique result: {critique_result},"
            f" should_stop={should_stop}"
        )
        yield Event(author=self.name, actions=EventActions(escalate=should_stop))


def experience_refinament_agent_factory(
    exp_type: ValidExperienceKeys, agent_id: str | None = None, max_iterations: int = 1
) -> SequentialAgent:
    # Use a unique agent ID if not provided
    if agent_id is None:
        agent_id = str(uuid.uuid4())[:8]

    example = json.dumps(EXAMPLES[exp_type], indent=2)
    schema_output = OUTPUT_SCHEMAS[exp_type]

    initial_experience_draft_agent = Agent(
        name=f"InitialExperienceDraftAgent_{agent_id}",
        model=experience_refiner_model,
        description=(
            "An agent that enhances a first draft of experience"
            " descriptions to better align them with job requirements and"
            " technology stack."
        ),
        instruction=PROMPT_INITIAL_EXP_ENHANCEMENT.format(
            agent_id=agent_id, example=example
        ),
        output_key=f"enhanced_experience_{agent_id}",
        output_schema=schema_output,
    )

    experience_critique_agent = Agent(
        name=f"ExperienceCritiqueAgent_{agent_id}",
        model=experience_critique_model,
        description=(
            "An agent that critiques and provides feedback on a draft of experience."
        ),
        instruction=PROMPT_CRITIC.format(agent_id=agent_id),
        output_key=f"critique_{agent_id}",
    )

    check_status_and_escalate_agent = CheckStatusAndEscalateAgent(
        name=f"CheckStatusAndEscalateAgent_{agent_id}",
        agent_id=agent_id,
    )

    experience_refiner_agent = Agent(
        name=f"ExperienceRefinerAgent_{agent_id}",
        model=experience_refiner_model,
        description=(
            "An agent that enhances a draft of experience descriptions based on"
            " feedback from a critic agent to better align them with job"
            " requirements and technology stack."
        ),
        instruction=PROMPT_REFINER_EXP_ENHANCEMENT.format(
            agent_id=agent_id, example=example
        ),
        output_key=f"enhanced_experience_{agent_id}",
        output_schema=schema_output,
    )

    refinement_loop_agent = LoopAgent(
        name=f"RefinementLoopAgent_{agent_id}",
        sub_agents=[
            experience_critique_agent,
            check_status_and_escalate_agent,
            experience_refiner_agent,
        ],
        max_iterations=max_iterations,
    )

    experience_enhancement_sequence = SequentialAgent(
        name=f"ExperienceRefinementSequence_{agent_id}",
        sub_agents=[
            initial_experience_draft_agent,
            refinement_loop_agent,
        ],
    )

    return experience_enhancement_sequence


class ExperienceEnhancementOrchestratorAgent(BaseAgent):
    """An agent that aggregates enhanced experiences from sub-agents."""

    max_refinement_iterations: int = 1

    @t.override
    async def _run_async_impl(self, ctx: InvocationContext) -> t.AsyncGenerator[Event]:
        logging.info(
            f"[{self.name}] Starting Experiences Enhancement Aggregator Agent."
        )

        retrived_exps: list[ExperienceRetrieval] = ctx.session.state.get(
            "retrieved_experiences", []
        )
        if not retrived_exps:
            logging.error(
                f"[{self.name}] No retrieved experiences found in session state."
            )
            return

        # Create a parallel agent to enhance each experience concurrently
        tagged_experiences: dict[str, ExperienceRetrieval] = {}
        parallel_sub_agents: list[SequentialAgent] = []
        for exp in retrived_exps:
            # We will tag each agent with the experience ID.
            agent_id = exp["exp_id"].replace(".", "_")

            # Save the experience description in the session state,
            #  to be used by the experience enhancement agents.
            ctx.session.state[f"experience_{agent_id}"] = exp["description"]

            # Create an experience enhancement agent for each experience
            enh_agent = experience_refinament_agent_factory(
                exp_type=exp["exp_type"],
                agent_id=agent_id,
                max_iterations=self.max_refinement_iterations,
            )

            # Finally, tag the experience for reference
            tagged_experiences[agent_id] = exp
            parallel_sub_agents.append(enh_agent)

        parallel_enhancement_agent = ParallelAgent(
            name="ParallelExperienceEnhancementAgent",
            sub_agents=parallel_sub_agents,
        )

        # Save tagged experiences in the session state for later reference
        ctx.session.state["tagged_experiences"] = tagged_experiences

        # Run the parallel enhancement agent
        async for event in parallel_enhancement_agent.run_async(ctx):
            yield event


experience_enhancement_orchestrator_agent = ExperienceEnhancementOrchestratorAgent(
    name="ExperienceEnhancementOrchestratorAgent",
    max_refinement_iterations=MAX_REFINEMENT_ITERATIONS,
)
