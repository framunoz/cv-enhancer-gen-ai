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


class ReferenceItemEssential(BaseModel):
    pass


class ReferenceItem(
    BaseModel,
):
    name: str | None = Field(
        None,
        description="Name of the reference",
    )
    reference: str | None = Field(
        None,
        description="Reference text or statement",
    )

    def get_essential(self) -> ReferenceItemEssential:
        return ReferenceItemEssential()

    __EXAMPLE__ = {
        "name": "Jane Doe",
        "reference": "Reference…",
    }


assert ReferenceItem.model_validate(ReferenceItem.__EXAMPLE__)  # noqa: S101
