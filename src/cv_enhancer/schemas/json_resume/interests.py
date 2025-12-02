"""
Schema for this part of the json resume:

```
  "interests": [{
    "name": "Wildlife",
    "keywords": [
      "Ferrets",
      "Unicorns"
    ]
  }],
```
"""

import typing as t

from pydantic import Field

from ..schemas_utils import consolidate_id, sanitize_text
from ._abc import JsonResumeBaseModel


class InterestItem(JsonResumeBaseModel):
    name: str | None = Field(
        None,
        description="Name of the interest",
    )
    keywords: list[str] | None = Field(
        None,
        description="List of keywords related to the interest",
    )

    @property
    def item_type(self) -> str:
        return "interests"

    __EXAMPLE__: t.ClassVar = {
        "name": "Wildlife",
        "keywords": [
            "Ferrets",
            "Unicorns",
        ],
    }

    @t.override
    def get_id(self) -> str:
        return consolidate_id(
            self.item_type,
            sanitize_text(self.name) if self.name else "unknown",
        )

    def format(self) -> str:
        return f"""
## Interest: {self.name}

- Keywords: {', '.join(self.keywords) if self.keywords else 'N/A'}
"""


assert InterestItem.model_validate(InterestItem.__EXAMPLE__)  # noqa: S101
