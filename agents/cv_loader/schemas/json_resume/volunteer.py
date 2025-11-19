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

import typing as t

from pydantic import BaseModel, Field, HttpUrl


class VolunteerItem(BaseModel):
    organization: str = Field(
        ...,
        description="Name of the organization",
    )
    position: str = Field(
        ...,
        description="Position held in the organization",
    )
    url: HttpUrl | t.Literal[""] = Field(
        ...,
        description="URL of the organization",
    )
    startDate: str = Field(
        ...,
        description="Start date of the volunteer position (YYYY-MM-DD)",
    )
    endDate: str | None = Field(
        None,
        description="End date of the volunteer position (YYYY-MM-DD)",
    )
    summary: str = Field(
        ...,
        description="Summary of the volunteer work",
    )
    highlights: list[str] = Field(
        default_factory=list,
        description="List of highlights or achievements during the volunteer work",
    )


__VOLUNTEER_ITEM_EXAMPLE = {
    "organization": "Organization",
    "position": "Volunteer",
    "url": "https://organization.com/",
    "startDate": "2012-01-01",
    "endDate": "2013-01-01",
    "summary": "Description…",
    "highlights": ["Awarded 'Volunteer of the Month'"],
}

assert VolunteerItem.model_validate(__VOLUNTEER_ITEM_EXAMPLE)  # noqa: S101
