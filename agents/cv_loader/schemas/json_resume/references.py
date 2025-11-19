"""
Schema for this part of the json resume:

```
  "references": [{
    "name": "Jane Doe",
    "reference": "Reference…"
  }],
```
"""

from pydantic import BaseModel, Field


class ReferenceItem(BaseModel):
    name: str | None = Field(
        None,
        description="Name of the reference",
    )
    reference: str | None = Field(
        None,
        description="Reference text or statement",
    )


__REFERENCE_ITEM_EXAMPLE = {
    "name": "Jane Doe",
    "reference": "Reference…",
}

assert ReferenceItem.model_validate(__REFERENCE_ITEM_EXAMPLE)  # noqa: S101
