"""
Schema for this part of the json resume:

```
  "awards": [{
    "title": "Award",
    "date": "2014-11-01",
    "awarder": "Company",
    "summary": "There is no spoon."
  }],
```
"""

import datetime as dt

from pydantic import BaseModel, Field


class AwardItem(BaseModel):
    title: str | None = Field(
        None,
        description="Title of the award",
    )
    date: dt.datetime | None = Field(
        None,
        description="Date when the award was received (YYYY-MM-DD)",
    )
    awarder: str | None = Field(
        None,
        description="Name of the organization or person who gave the award",
    )
    summary: str | None = Field(
        None,
        description="Summary or description of the award",
    )

    __EXAMPLE__ = {
        "title": "Award",
        "date": "2014-11-01",
        "awarder": "Company",
        "summary": "There is no spoon.",
    }

    def format(self) -> str:
        return (
            f"Award: {self.title}\n"
            f"Date: {self.date.date() if self.date else 'N/A'}\n"
            f"Awarder: {self.awarder}\n"
            f"Summary: {self.summary}\n"
        )


assert AwardItem.model_validate(AwardItem.__EXAMPLE__)  # noqa: S101
