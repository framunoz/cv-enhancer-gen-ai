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


class AwardItemEssential(BaseModel):
    title: str | None = Field(
        None,
        description="Title of the award",
    )
    summary: str | None = Field(
        None,
        description="Summary or description of the award",
    )


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

    def get_essential(self) -> AwardItemEssential:
        return AwardItemEssential(
            title=self.title,
            summary=self.summary,
        )

    __EXAMPLE__ = {
        "title": "Award",
        "date": "2014-11-01",
        "awarder": "Company",
        "summary": "There is no spoon.",
    }


assert AwardItem.model_validate(AwardItem.__EXAMPLE__)  # noqa: S101
