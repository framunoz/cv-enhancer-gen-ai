"""
Schema for this part of the json resume:

```
  "work": [{
    "name": "Company",
    "position": "President",
    "url": "https://company.com",
    "startDate": "2013-01-01",
    "endDate": "2014-01-01",
    "summary": "Description…",
    "highlights": [
      "Started the company"
    ]
  }],
```
"""

import datetime as dt
import typing as t

from pydantic import BaseModel, Field, HttpUrl


class WorkItemEssential(BaseModel):
    name: str | None = Field(
        None,
        description="Name of the company or organization",
    )
    position: str | None = Field(
        None,
        description="Position held at the company",
    )
    summary: str | None = Field(
        None,
        description="Summary of the role and responsibilities",
    )
    highlights: list[str] | None = Field(
        None,
        description="List of highlights or achievements in this role",
    )


class WorkItem(
    BaseModel,
):
    name: str | None = Field(
        None,
        description="Name of the company or organization",
    )
    position: str | None = Field(
        None,
        description="Position held at the company",
    )
    url: HttpUrl | t.Literal[""] | None = Field(
        None,
        description="URL of the company or organization",
    )
    startDate: dt.datetime | None = Field(
        None,
        description="Start date of the position (YYYY-MM-DD)",
    )
    endDate: dt.datetime | None = Field(
        None,
        description="End date of the position (YYYY-MM-DD)",
    )
    summary: str | None = Field(
        None,
        description="Summary of the role and responsibilities",
    )
    highlights: list[str] | None = Field(
        None,
        description="List of highlights or achievements in this role",
    )
    keywords: list[str] | None = Field(
        None,
        description="List of keywords extracted from the work item",
    )

    def get_essential(self) -> WorkItemEssential:
        return WorkItemEssential(
            name=self.name,
            position=self.position,
            summary=self.summary,
            highlights=self.highlights,
        )

    __EXAMPLE__ = {
        "name": "Company",
        "position": "President",
        "url": "https://company.com",
        "startDate": "2013-01-01",
        "endDate": "2014-01-01",
        "summary": "Description…",
        "highlights": ["Started the company"],
    }
