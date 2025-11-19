"""
Schema for this part of the json resume:

```
  "languages": [{
    "language": "English",
    "fluency": "Native speaker"
  }],
```
"""

from pydantic import BaseModel, Field


class LanguageItem(BaseModel):
    language: str | None = Field(
        None,
        description="Name of the language",
    )
    fluency: str | None = Field(
        None,
        description="Fluency level in the language",
    )


__LANGUAGE_ITEM_EXAMPLE = {
    "language": "English",
    "fluency": "Native speaker",
}


assert LanguageItem.model_validate(__LANGUAGE_ITEM_EXAMPLE)  # noqa: S101
