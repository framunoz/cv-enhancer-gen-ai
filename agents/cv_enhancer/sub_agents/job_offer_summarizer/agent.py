import json

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

from .schemas import __SCHEMA_EXAMPLE, JobOfferSummarized

MODEL = "gemini-2.5-flash"

PROMPT = f"""
You are a Job Offer Summarizer. Your only task is to read the provided job offer
and extract the key information such as the description, requirements, stack
and provide a concise summary. Do not add any additional information
(such as benefits, the title, the company) or opinions.

The output must be only the summarized job offer without any additional
commentary.

Here is an example of the output format:
---
{json.dumps(__SCHEMA_EXAMPLE, indent=2)}
---
"""

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

job_offer_summarizer_agent = Agent(
    name="JobOfferSummarizerAgent",
    model=Gemini(
        model=MODEL,
        retry_options=retry_config,
    ),
    description=(
        "An agent that summarizes job offers by extracting key information and"
        " presenting it clearly to assist job seekers in understanding"
        " the opportunities."
    ),
    instruction=PROMPT,
    output_key="summarized_job_offer",
    output_schema=JobOfferSummarized,
)

# Expose the agent for external use
root_agent = job_offer_summarizer_agent
