from enum import StrEnum


class GeminiModels(StrEnum):
    """
    Enumeration of Gemini model names.

    Expand this enumeration as new models become available. The model names
    can be found in the [Gemini API documentation](https://ai.google.dev/gemini-api/docs/pricing).
    """

    GEMINI_3_PRO_PREVIEW = "gemini-3-pro-preview"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"
