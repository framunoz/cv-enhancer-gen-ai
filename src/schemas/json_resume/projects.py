"""
Schema for this part of the json resume:

```
  "projects": [{
    "name": "Project",
    "startDate": "2019-01-01",
    "endDate": "2021-01-01",
    "description": "Description...",
    "highlights": [
      "Won award at AIHacks 2016"
    ],
    "url": "https://project.com/"
  }]
```
"""

import datetime as dt
import typing as t

from pydantic import BaseModel, Field, HttpUrl


class ProjectItem(BaseModel):
    name: str | None = Field(
        None,
        description="Name of the project",
    )
    startDate: dt.datetime | None = Field(
        None,
        description="Start date of the project (YYYY-MM-DD)",
    )
    endDate: dt.datetime | None = Field(
        None,
        description="End date of the project (YYYY-MM-DD)",
    )
    description: str | None = Field(
        None,
        description="Description of the project",
    )
    highlights: list[str] | None = Field(
        None,
        description="List of highlights or achievements in the project",
    )
    url: HttpUrl | t.Literal[""] | None = Field(
        None,
        description="URL of the project",
    )
    keywords: list[str] | None = Field(
        None,
        description="List of keywords extracted from the project item",
    )

    __EXAMPLE__ = {
        "name": "Project",
        "startDate": "2019-01-01",
        "endDate": "2021-01-01",
        "description": "Description...",
        "highlights": ["Won award at AIHacks 2016"],
        "url": "https://project.com/",
    }

    def format(self) -> str:
        return (
            f"Project: {self.name}\n"
            f"Start Date: {self.startDate.date() if self.startDate else 'N/A'}\n"
            f"End Date: {self.endDate.date() if self.endDate else 'N/A'}\n"
            f"Description: {self.description}\n"
            f"Highlights: {', '.join(self.highlights) if self.highlights else 'N/A'}\n"
            f"URL: {self.url}\n"
        )


assert ProjectItem.model_validate(ProjectItem.__EXAMPLE__)  # noqa: S101
