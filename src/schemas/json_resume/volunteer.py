"""
Schema for this part of the json resume:

```
  "volunteer": [{
    "organization": "Organization",
    "position": "Volunteer",
    "url": "https://organization.com/",
    "startDate": "2012-01-01",
    "endDate": "2013-01-01",
    "summary": "Description…",
    "highlights": [
      "Awarded 'Volunteer of the Month'"
    ]
  }],
```
"""

import datetime as dt
import typing as t

from pydantic import BaseModel, Field, HttpUrl


class VolunteerItem(BaseModel):
    organization: str | None = Field(
        None,
        description="Name of the organization",
    )
    position: str | None = Field(
        None,
        description="Position held in the organization",
    )
    url: HttpUrl | t.Literal[""] | None = Field(
        None,
        description="URL of the organization",
    )
    startDate: dt.datetime | None = Field(
        None,
        description="Start date of the volunteer position (YYYY-MM-DD)",
    )
    endDate: dt.datetime | None = Field(
        None,
        description="End date of the volunteer position (YYYY-MM-DD)",
    )
    summary: str | None = Field(
        None,
        description="Summary of the volunteer work",
    )
    highlights: list[str] | None = Field(
        None,
        description="List of highlights or achievements during the volunteer work",
    )

    __EXAMPLE__ = {
        "organization": "Organization",
        "position": "Volunteer",
        "url": "https://organization.com/",
        "startDate": "2012-01-01",
        "endDate": "2013-01-01",
        "summary": "Description…",
        "highlights": ["Awarded 'Volunteer of the Month'"],
    }

    def format(self) -> str:
        return (
            f"Organization: {self.organization}\n"
            f"Position: {self.position}\n"
            f"URL: {self.url}\n"
            f"Start Date: {self.startDate.date() if self.startDate else 'N/A'}\n"
            f"End Date: {self.endDate.date() if self.endDate else 'N/A'}\n"
            f"Summary: {self.summary}\n"
            f"Highlights: {', '.join(self.highlights) if self.highlights else 'N/A'}\n"
        )


assert VolunteerItem.model_validate(VolunteerItem.__EXAMPLE__)  # noqa: S101
