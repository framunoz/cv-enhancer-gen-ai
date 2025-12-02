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

from pydantic import Field, HttpUrl

from ..schemas_utils import consolidate_id, sanitize_text
from ._abc import JsonResumeFormattableBaseModel


class WorkItem(JsonResumeFormattableBaseModel):
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

    @property
    def item_type(self) -> str:
        return "work"

    __EXAMPLE__: t.ClassVar = {
        "name": "Company",
        "position": "President",
        "url": "https://company.com",
        "startDate": "2013-01-01",
        "endDate": "2014-01-01",
        "summary": "Description…",
        "highlights": ["Started the company"],
        "keywords": ["leadership", "entrepreneurship"],
    }

    @t.override
    def get_id(self) -> str:
        return consolidate_id(
            self.item_type,
            self.startDate.strftime("%Y%m%d") if self.startDate else "no_date",
            sanitize_text(self.name or "no_company", max_len=10),
            sanitize_text(self.position or "no_position", max_len=10),
        )

    @t.override
    def format(self) -> str:
        highlights_formatted = ""
        if self.highlights:
            for highlight in self.highlights:
                highlights_formatted += f"    - {highlight}\n"
        else:
            highlights_formatted = "N/A"
        return f"""
## Company: {self.name}

### Position: {self.position}

- Summary:
    > {self.summary}

- Highlights:
{highlights_formatted}

- Keywords: {', '.join(self.keywords) if self.keywords else 'N/A'}
"""
