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
    name: str = Field(
        ...,
        description="Name of the project",
    )
    startDate: dt.datetime = Field(
        ...,
        description="Start date of the project (YYYY-MM-DD)",
    )
    endDate: dt.datetime | None = Field(
        None,
        description="End date of the project (YYYY-MM-DD)",
    )
    description: str = Field(
        ...,
        description="Description of the project",
    )
    highlights: list[str] = Field(
        default_factory=list,
        description="List of highlights or achievements in the project",
    )
    url: HttpUrl | t.Literal[""] = Field(
        ...,
        description="URL of the project",
    )


__PROJECT_ITEM_EXAMPLE = {
    "name": "Project",
    "startDate": "2019-01-01",
    "endDate": "2021-01-01",
    "description": "Description...",
    "highlights": ["Won award at AIHacks 2016"],
    "url": "https://project.com/",
}

assert ProjectItem.model_validate(__PROJECT_ITEM_EXAMPLE)  # noqa: S101
