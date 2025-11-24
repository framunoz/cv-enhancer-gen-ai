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


class LanguageItemEssential(BaseModel):
    pass


class LanguageItem(
    BaseModel,
):
    language: str | None = Field(
        None,
        description="Name of the language",
    )
    fluency: str | None = Field(
        None,
        description="Fluency level in the language",
    )

    def get_essential(self) -> LanguageItemEssential:
        return LanguageItemEssential()

    __EXAMPLE__ = {
        "language": "English",
        "fluency": "Native speaker",
    }


assert LanguageItem.model_validate(LanguageItem.__EXAMPLE__)  # noqa: S101
