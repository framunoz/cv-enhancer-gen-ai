"""
Schema for this part of the json resume:

```
  "languages": [{
    "language": "English",
    "fluency": "Native speaker"
  }],
```
"""

import typing as t

from pydantic import Field

from ..schemas_utils import consolidate_id, sanitize_text
from ._abc import JsonResumeBaseModel


class LanguageItem(JsonResumeBaseModel):
    language: str | None = Field(
        None,
        description="Name of the language",
    )
    fluency: str | None = Field(
        None,
        description="Fluency level in the language",
    )

    @property
    def item_type(self) -> str:
        return "languages"

    @t.override
    def get_id(self) -> str:
        return consolidate_id(
            self.item_type,
            sanitize_text(self.language) if self.language else "unknown",
        )

    __EXAMPLE__: t.ClassVar = {
        "language": "English",
        "fluency": "Native speaker",
    }


assert LanguageItem.model_validate(LanguageItem.__EXAMPLE__)  # noqa: S101
