"""
Schema for this part of the json resume:

```
  "references": [{
    "name": "Jane Doe",
    "reference": "Reference…"
  }],
```
"""

import typing as t

from pydantic import Field

from ..schemas_utils import consolidate_id, sanitize_text
from ._abc import JsonResumeBaseModel


class ReferenceItem(JsonResumeBaseModel):
    name: str | None = Field(
        None,
        description="Name of the reference",
    )
    reference: str | None = Field(
        None,
        description="Reference text or statement",
    )

    @property
    def item_type(self) -> str:
        return "references"

    @t.override
    def get_id(self) -> str:
        return consolidate_id(
            self.item_type,
            sanitize_text(self.name) if self.name else "unknown",
        )

    __EXAMPLE__: t.ClassVar = {
        "name": "Jane Doe",
        "reference": "Reference…",
    }


assert ReferenceItem.model_validate(ReferenceItem.__EXAMPLE__)  # noqa: S101
