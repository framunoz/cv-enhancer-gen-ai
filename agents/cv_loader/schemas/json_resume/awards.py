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
    title: str = Field(
        ...,
        description="Title of the award",
    )
    date: dt.datetime = Field(
        ...,
        description="Date when the award was received (YYYY-MM-DD)",
    )
    awarder: str = Field(
        ...,
        description="Name of the organization or person who gave the award",
    )
    summary: str | None = Field(
        None,
        description="Summary or description of the award",
    )


__AWARD_ITEM_EXAMPLE = {
    "title": "Award",
    "date": "2014-11-01",
    "awarder": "Company",
    "summary": "There is no spoon.",
}

assert AwardItem.model_validate(__AWARD_ITEM_EXAMPLE)  # noqa: S101
