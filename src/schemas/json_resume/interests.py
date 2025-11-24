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


class InterestItemEssential(BaseModel):
    name: str | None = Field(
        None,
        description="Name of the interest",
    )
    keywords: list[str] | None = Field(
        None,
        description="List of keywords related to the interest",
    )


class InterestItem(
    BaseModel,
):
    name: str | None = Field(
        None,
        description="Name of the interest",
    )
    keywords: list[str] | None = Field(
        None,
        description="List of keywords related to the interest",
    )

    def get_essential(self) -> InterestItemEssential:
        return InterestItemEssential(
            name=self.name,
            keywords=self.keywords,
        )

    __EXAMPLE__ = {
        "name": "Wildlife",
        "keywords": [
            "Ferrets",
            "Unicorns",
        ],
    }


assert InterestItem.model_validate(InterestItem.__EXAMPLE__)  # noqa: S101
