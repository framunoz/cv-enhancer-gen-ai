import os

from google.adk.models.google_llm import Gemini
from google.genai import types

os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


class CvSaverConfig:

    cv_saver_model: Gemini = Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config,
    )

    stack_adder_model: Gemini = Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    )


config = CvSaverConfig()
