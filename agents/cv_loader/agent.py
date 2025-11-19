from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from .prompt import PROMPT

MODEL = "gemini-2.5-flash"

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

cv_loader_agent = LlmAgent(
    model=Gemini(
        model=MODEL,
        retry_options=retry_config,
    ),
    name="CVLoaderAgent",
    description="An agent that writes a CV based on the job offer and user profile.",
    instruction=PROMPT,
)

root_agent = cv_loader_agent
