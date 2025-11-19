from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

MODEL = "gemini-2.5-flash"

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


retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

writer_agent = Agent(
    model=Gemini(
        model=MODEL,
        retry_options=retry_config,
    ),
    name="WriterAgent",
    description="An agent that writes a CV based on the job offer and user profile.",
    instruction=PROMPT,
)

root_agent = writer_agent
