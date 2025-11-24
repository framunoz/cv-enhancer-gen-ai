import json
import logging
import typing as t

from google.adk.agents import BaseAgent
from google.adk.agents.base_agent import BaseAgentState
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents.llm_agent import LlmAgent
from google.adk.events import Event, EventActions
from google.adk.utils.context_utils import Aclosing
from rich import print as rprint
from rich.logging import RichHandler

from . import tools
from .config import config
from .schemas.json_resume.json_resume import JsonResume

logger = logging.getLogger(__name__)
# Clean previous handlers
logger.handlers = []
logger.addHandler(RichHandler())

class StackAdderOrchestratorAgent(BaseAgent):
    """Orchestrator agent for Stack Adder functionality."""

    @t.override
    async def _run_async_impl(  # type: ignore[override]
        self, ctx: InvocationContext
    ) -> t.AsyncGenerator[Event]:  # type: ignore[override]
        logger.debug(f"{ctx.session.state=}")
        rprint(f"{ctx.session.state=}")
        logger.debug(f"{ctx.session=}")
        event = ctx.session.events[-1]
        logger.debug(f"Event: {event}")
        content = event.content
        if content is None:
            return
        logger.debug(f"Event content: {content}")
        parts = content.parts
        if parts is None:
            return
        logger.debug(f"Event parts: {parts}")
        part = parts[0]
        logger.debug(f"Event part: {part}")
        part_text = part.text
        if part_text is None:
            pass
        logger.info(f"Event part_text: {part_text}")
        inline_data = part.inline_data
        if inline_data is None:
            return
        logger.debug(f"Event inline_data: {inline_data}")
        data = inline_data.data
        if data is None:
            return
        try:
            json_resume = JsonResume.model_validate_json(data)
            logger.info("Parsed JSON Resume: %s", json_resume)
            json_resume_ = json_resume.get_essential()
            logger.info("Essential JSON Resume: %s", json_resume_)
            tools.save_cv_as_json(json_resume_.model_dump_json())
        except Exception as e:
            logger.error("Failed to parse JSON Resume: %s", e)
            return

        yield Event(
            author=self.name,
        )
        return
        agent_state = self._load_agent_state(ctx, BaseAgentState)
        logger.debug("Starting StackAdderOrchestratorAgent with state: %s", agent_state)

        logger.debug(f"{ctx.input_realtime_cache=}")
        logger.debug(f"{ctx.is_resumable=}")
        events = ctx._get_events(current_invocation=True, current_branch=True)
        if events and (
            ctx.should_pause_invocation(events[-1])
            or ctx.should_pause_invocation(events[-2])
        ):
            return
        # Only yield an end state if the last event is no longer a long running
        # tool call.
        ctx.set_agent_state(self.name, end_of_agent=True)
        yield self._create_agent_state_event(ctx)

root_agent = StackAdderOrchestratorAgent(
    name="StackAdderOrchestratorAgent",
    description="Orchestrator agent for Stack Adder functionality.",
)


MODEL = "gemini-2.5-flash"

PROMPT = f"""
You are a CV Saver Agent.

You must to follow these steps:
1. Receive the CV in a text format.
2. Convert the CV to JSON format using the schema provided.
3. Save the CV using the 'save_cv_as_json' tool.

Json Resume Schema:
```json
{json.dumps(JsonResume.__EXAMPLE__, indent=2)}
```
"""

# logger.debug("Initializing CV Saver Agent with model: %s", MODEL)
# logger.debug("Using prompt: %s", PROMPT)

cv_loader_agent = LlmAgent(
    model=config.cv_saver_model,
    name="CVLoaderAgent",
    description="An agent that writes a CV based on the job offer and user profile.",
    instruction=PROMPT,
    tools=[tools.save_cv_as_json],
)

# root_agent = cv_loader_agent
