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
    name: str | None = Field(
        None,
        description="Name of the interest",
    )
    keywords: list[str] | None = Field(
        None,
        description="List of keywords related to the interest",
    )

    __EXAMPLE__ = {
        "name": "Wildlife",
        "keywords": [
            "Ferrets",
            "Unicorns",
        ],
    }

    def format(self) -> str:
        return (
            f"Interest: {self.name}\n"
            f"Keywords: {', '.join(self.keywords) if self.keywords else 'N/A'}\n"
        )


assert InterestItem.model_validate(InterestItem.__EXAMPLE__)  # noqa: S101
