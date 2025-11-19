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
    name: str = Field(
        ...,
        description="Name of the reference",
    )
    reference: str = Field(
        ...,
        description="Reference text or statement",
    )


__REFERENCE_ITEM_EXAMPLE = {
    "name": "Jane Doe",
    "reference": "Reference…",
}

assert ReferenceItem.model_validate(__REFERENCE_ITEM_EXAMPLE)  # noqa: S101
