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

from pydantic import BaseModel, Field


class InterestItem(BaseModel):
    name: str = Field(
        ...,
        description="Name of the interest",
    )
    keywords: list[str] = Field(
        default_factory=list,
        description="List of keywords related to the interest",
    )


__INTEREST_ITEM_EXAMPLE = {
    "name": "Wildlife",
    "keywords": [
        "Ferrets",
        "Unicorns",
    ],
}

assert InterestItem.model_validate(__INTEREST_ITEM_EXAMPLE)  # noqa: S101
