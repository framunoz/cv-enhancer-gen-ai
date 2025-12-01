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

from ..schemas_utils import consolidate_id, sanitize_text


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

    @property
    def item_type(self) -> str:
        return "project"

    __EXAMPLE__ = {
        "name": "Project",
        "startDate": "2019-01-01",
        "endDate": "2021-01-01",
        "description": "Description...",
        "highlights": ["Won award at AIHacks 2016"],
        "url": "https://project.com/",
        "keywords": ["project", "achievement"],
    }

    def get_id(self) -> str:
        return consolidate_id(
            "project",
            sanitize_text(self.name or "no_project", max_len=10),
            self.startDate.strftime("%Y%m") if self.startDate else "no_date",
        )

    def format(self) -> str:
        highlights_formatted = ""
        if self.highlights:
            for highlight in self.highlights:
                highlights_formatted += f"    - {highlight}\n"
        else:
            highlights_formatted = "N/A"
        return f"""
## Project: {self.name}

- Description:
    > {self.description}

- Highlights:
{highlights_formatted}

- Keywords: {', '.join(self.keywords) if self.keywords else 'N/A'}
"""


assert ProjectItem.model_validate(ProjectItem.__EXAMPLE__)  # noqa: S101
