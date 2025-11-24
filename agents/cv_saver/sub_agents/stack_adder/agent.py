from google.adk.agents.llm_agent import Agent

from ...config import config

PROMPT = """
You are a Writer Agent. Your task is to elaborate a CV based on the provided
job offer and user profile. Use the job offer to tailor the CV content to match
the requirements and desired skills. Ensure the CV is well-structured, clear,
concise, and tailored to the specific job application.

Job Offer:
---
{summarized_job_offer}
---


Please provide the user profile details to proceed with the CV elaboration.

"""

writer_agent = Agent(
    model=config.stack_adder_model,
    name="StackAdderAgent",
    description="An agent that writes a CV based on the job offer and user profile.",
    instruction=PROMPT,
)

root_agent = writer_agent
