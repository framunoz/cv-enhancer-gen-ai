import json

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

from cv_enhancer.schemas import JobOfferSummarized

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    initial_delay=1,
    max_delay=60,  # Maximum delay between retries
    exp_base=3,  # Delay multiplier
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


PROMPT = f"""
You are a Job Offer Summarizer. Your only task is to read the provided job offer
and extract the key information such as the description, requirements, stack
and provide a concise summary. Do not add any additional information
(such as benefits, the title, the company...) or opinions. Try to summarize
in 300 words maximum.

Try to be as specific as possible when extracting the tech stack.

Here is an example of the output format:
---
{json.dumps(JobOfferSummarized.__EXAMPLE__, indent=2)}
---

You MUST RETURN the output in the EXACT FORMAT as shown above, without any additional text.

Mantain the original language of the job offer.
"""


job_offer_analyzer_model = Gemini(
    model="gemini-2.5-flash-preview-09-2025",
    retry_options=retry_config,
)

job_offer_analyzer_agent = Agent(
    name="JobOfferAnalyzerAgent",
    model=job_offer_analyzer_model,
    description=(
        "An agent that summarizes job offers by extracting key information and"
        " presenting it clearly to assist job seekers in understanding"
        " the opportunities."
    ),
    instruction=PROMPT,
    output_key="summarized_job_offer",
    output_schema=JobOfferSummarized,
)

root_agent = job_offer_analyzer_agent
