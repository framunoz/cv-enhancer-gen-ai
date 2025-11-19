from google.adk.agents.sequential_agent import SequentialAgent

from .sub_agents.job_offer_summarizer import job_offer_summarizer_agent
from .sub_agents.writer import writer_agent

cv_enhancer_agent = SequentialAgent(
    name="CVEnhancerAgent",
    description=(
        "An agent that enhances CVs by improving language, formatting, and "
        "tailoring content to specific job descriptions."
    ),
    sub_agents=[
        job_offer_summarizer_agent,
        writer_agent,
    ],
)

# Expose the agent for external use
root_agent = cv_enhancer_agent
