import collections as c
import logging
import typing as t

from google.adk.agents import Agent, BaseAgent, ParallelAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.models.google_llm import Gemini
from google.genai import types
from pydantic import BaseModel, Field

from ...tools.rag import (
    ValidExperienceKeys,
    retrieve_experiences_by_query,
)


class ExperienceLimits(t.TypedDict, total=False):
    """Limits for the number of experiences to enhance in each category."""

    work: int
    volunteer: int
    certificates: int
    projects: int
    skills: int
    interests: int


EXPERIENCE_LIMITS = ExperienceLimits(
    work=3,
    projects=1,
)


class ExperiencesSelected(BaseModel):
    experiences_selected: list[str] = Field(
        ...,
        description="List of experience IDs selected to be enhanced",
    )
    __EXAMPLE__: t.ClassVar = {
        "experiences_selected": ["work_1", "project_3", "skill_2"],
    }


retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    initial_delay=1,
    max_delay=60,  # Maximum delay between retries
    exp_base=3,  # Delay multiplier
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

experience_selector_models = Gemini(
    model="gemini-2.5-flash-lite-preview-09-2025",
    retry_options=retry_config,
)


PROMPT = """
You are a talent recruiter who knows how to select the best experiences
from a resume for a specific job position. Your task is to select key
experiences from a resume that align with a given job posting.
You should consider the job description, requirements, and technology
stack mentioned in the job posting.

Job Offer Summary:
{{summarized_job_offer}}

Experiences to consider:
{{experiences_{exp_type}}}

Max number of experiences to select: {{max_experiences_{exp_type}}}

Your output should be a list of ids (the `exp_id` field) of the selected experiences,
formatted as the following JSON object:
---
{{"experiences_selected": ["exp_id_1", "exp_id_2"]}}
---
Make sure to return the output in the EXACT FORMAT as shown above, without any additional text.
"""


def create_experience_selector_agent(
    exp_type: ValidExperienceKeys,
) -> Agent:
    """Create an Experience Selector Agent for a specific experience type.

    Args:
        exp_type (ValidExperienceKeys): The type of experience the agent will select.

    Returns:
        Agent: The configured Experience Selector Agent.
    """

    agent = Agent(
        name=f"ExperienceSelectorAgent_{exp_type}",
        model=experience_selector_models,
        description=(
            f"An agent that selects the most relevant {exp_type} experiences"
            " from a resume based on a job posting."
        ),
        instruction=PROMPT.format(exp_type=exp_type),
        output_key=f"experiences_selected_{exp_type}",
        output_schema=ExperiencesSelected,
    )

    return agent


class ExperienceRetrieverAgent(BaseAgent):
    """An agent that retrieves the most relevant experiences and saves them in the session state."""

    experience_limits: ExperienceLimits | None = None
    gap: int = 2

    @t.override
    async def _run_async_impl(  # noqa: PLR0912
        self, ctx: InvocationContext
    ) -> t.AsyncGenerator[Event]:
        logging.info(f"[{self.name}] Starting Experience Retrieval Agent")

        # Get the search query from the session state
        query = ctx.session.state.get("search_query", None)
        if query is None:
            logging.error(f"[{self.name}] No search query found in session state.")
            return

        # Retrieve the experiences using the retrieve_experiences_by_query tool
        #  from the session state
        retrieved_exps_result = retrieve_experiences_by_query(
            query=query, exp_type="all", n_results=0
        )

        if retrieved_exps_result.get("status") != "success":
            logging.error(
                f"[{self.name}] Failed to retrieve experiences:"
                f" {retrieved_exps_result.get('message')}"
            )
            return

        retrieved_exps = retrieved_exps_result["retrieved_experiences"]
        retrieved_exps_by_type = c.defaultdict(list)
        for exp in retrieved_exps:
            exp_type = exp["exp_type"]
            retrieved_exps_by_type[exp_type].append(exp)

        # Selectively limit experiences by type if limits are provided
        if self.experience_limits:
            # Delete experience types that are not in the limits
            for exp_type in list(retrieved_exps_by_type):
                if exp_type not in self.experience_limits:
                    del retrieved_exps_by_type[exp_type]

            # Limit experiences per type
            exp_selector_agents: dict[ValidExperienceKeys, Agent] = {}
            for exp_type, exps in retrieved_exps_by_type.items():
                exp_type: ValidExperienceKeys
                # Skip if no limit is set for this experience type
                if exp_type not in self.experience_limits:
                    continue

                # If currently there are less or equal experiences than
                #  the limit, skip limiting assisted with an agent
                limit = self.experience_limits[exp_type]
                if len(exps) <= limit:
                    continue

                # Otherwise, save in the session state the experiences
                #  to be selected and the maximum number allowed
                ctx.session.state[f"experiences_{exp_type}"] = exps[: limit + self.gap]
                ctx.session.state[f"max_experiences_{exp_type}"] = limit
                exp_selector_agents[exp_type] = create_experience_selector_agent(
                    exp_type
                )

            # Run in parallel the experience selector agents to select the experiences
            if exp_selector_agents:
                selector_agent_parallel = ParallelAgent(
                    name="ExperienceSelectorParallelAgent",
                    sub_agents=list(exp_selector_agents.values()),
                )

                async for event in selector_agent_parallel.run_async(ctx):
                    yield event

                # Update the retrieved experiences based on the selected ones
                for exp_type in exp_selector_agents:
                    selected_exp_ids: list[str] = ctx.session.state.get(
                        f"experiences_selected_{exp_type}", []
                    )["experiences_selected"]
                    selected_exps = [
                        exp
                        for exp in retrieved_exps_by_type[exp_type]
                        if exp["exp_id"] in selected_exp_ids
                    ]
                    retrieved_exps_by_type[exp_type] = selected_exps

        # Flatten the retrieved experiences by type
        retrieved_exps = []
        for exps in retrieved_exps_by_type.values():
            retrieved_exps.extend(exps)

        # Sort experiences by exp_id in descending order to display
        #  the most recent ones first.
        retrieved_exps.sort(key=lambda x: x["exp_id"], reverse=True)

        # Save the retrieved experiences in the session state
        ctx.session.state["retrieved_experiences"] = retrieved_exps

        logging.info(
            f"[{self.name}] Retrieved {len(retrieved_exps)} experiences for"
            " enhancement."
        )
        logging.debug(f"[{self.name}] Experiences: {retrieved_exps}")

        yield Event(author=self.name)


experience_retriever_agent = ExperienceRetrieverAgent(
    name="ExperienceRetrieverAgent",
    experience_limits=EXPERIENCE_LIMITS,
)
