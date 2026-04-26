import logging
import typing as t

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event

from cv_enhancer.schemas import JsonResume

from ...tools.rag import ExperienceRetrieval
from ...utils import get_json_resume


class EnhancedCvAssemblyAgent(BaseAgent):
    """This agent enhances a CV based on the job offer summary and
    retrieved experiences.
    """

    json_resume_template: JsonResume

    @t.override
    async def _run_async_impl(self, ctx: InvocationContext) -> t.AsyncGenerator[Event]:
        logging.info(f"[{self.name}] Starting CV Builder Agent.")

        # Get tagged experiences from the session state
        tagged_experiences = t.cast(
            dict[str, ExperienceRetrieval],
            ctx.session.state.get("tagged_experiences", {}),
        )

        # Get enhanced experiences from the session state
        enhanced_experiences: dict[str, dict[str, t.Any]] = {}
        for agent_id in tagged_experiences:
            enhanced_exp = t.cast(
                dict[str, t.Any],
                ctx.session.state.get(f"enhanced_experience_{agent_id}"),
            )
            enhanced_experiences[agent_id] = enhanced_exp

        # Build a json resume with the enhanced experiences
        json_resume_enhanced: dict[str, dict | list] = {}

        # Include basics from the template. It's assumed to be unchanged.
        if basics := self.json_resume_template.basics:
            json_resume_enhanced["basics"] = basics.model_dump()

        # Modify experiences with the enhanced versions
        for agent_id, enhanced_exp in enhanced_experiences.items():
            exp_id = tagged_experiences[agent_id]["exp_id"]
            exp_type = tagged_experiences[agent_id]["exp_type"]
            if exp_type not in json_resume_enhanced:
                json_resume_enhanced[exp_type] = []

            experience_obj = self.json_resume_template.find_experience(exp_id)
            if experience_obj:
                experience_dict = experience_obj.model_dump()
                for field, value in enhanced_exp.items():
                    experience_dict[field] = value
                json_resume_enhanced[exp_type].append(experience_dict)  # type: ignore

        enhanced_cv = JsonResume(**json_resume_enhanced)
        ctx.session.state["enhanced_cv"] = enhanced_cv

        yield Event(
            author=self.name,
            content={"parts": [{"text": enhanced_cv.model_dump_json(indent=2)}]},
        )


enhanced_cv_assembly_agent = EnhancedCvAssemblyAgent(
    name="EnhancedCvAssemblyAgent",
    json_resume_template=get_json_resume(),
)
