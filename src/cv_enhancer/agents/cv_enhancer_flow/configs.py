import typing as t
from dataclasses import dataclass

from google.adk.models.base_llm import BaseLlm
from google.adk.models.google_llm import Gemini
from google.genai import types

from ._models import GeminiModels
from ._singleton import _SingletonMeta

retry_config = types.HttpRetryOptions(
    attempts=100,  # Maximum retry attempts
    initial_delay=1,
    max_delay=60,  # Maximum delay between retries
    exp_base=3,  # Delay multiplier
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


class ExperienceLimits(t.TypedDict, total=False):
    """Limits for the number of experiences to enhance in each category."""

    work: int
    volunteer: int
    certificates: int
    projects: int
    skills: int
    interests: int


@dataclass
class CvSaverConfig(metaclass=_SingletonMeta):
    """
    Configuration for the agents used in the CV Enhancer flow.
    """

    # Models
    job_offer_analyzer_model: BaseLlm
    experience_refiner_model: BaseLlm
    experience_critique_model: BaseLlm
    experience_query_builder_model: BaseLlm

    # Embedding configuration
    embedding_model: str = "models/text-embedding-004"
    embedding_output_dim: int = 768


config: CvSaverConfig = CvSaverConfig(
    job_offer_analyzer_model=Gemini(
        model=GeminiModels.GEMINI_2_5_FLASH,
        retry_options=retry_config,
    ),
    experience_refiner_model=Gemini(
        model=GeminiModels.GEMINI_2_5_FLASH,
        retry_options=retry_config,
    ),
    experience_critique_model=Gemini(
        model=GeminiModels.GEMINI_2_5_PRO,
        retry_options=retry_config,
    ),
    experience_query_builder_model=Gemini(
        model=GeminiModels.GEMINI_2_5_FLASH_LITE,
        retry_options=retry_config,
    ),
)
