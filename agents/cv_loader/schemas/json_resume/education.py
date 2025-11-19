"""
Schema for this part of the json resume:

```
  "education": [{
    "institution": "University",
    "url": "https://institution.com/",
    "area": "Software Development",
    "studyType": "Bachelor",
    "startDate": "2011-01-01",
    "endDate": "2013-01-01",
    "score": "4.0",
    "courses": [
      "DB1101 - Basic SQL"
    ]
  }],
```
"""

import datetime as dt
import typing as t

from pydantic import BaseModel, Field, HttpUrl


class EducationItem(BaseModel):
    institution: str = Field(
        ...,
        description="Name of the educational institution",
    )
    url: HttpUrl | t.Literal[""] = Field(
        ...,
        description="URL of the educational institution",
    )
    area: str = Field(
        ...,
        description="Area of study",
    )
    studyType: str = Field(
        ...,
        description="Type of study (e.g., Bachelor, Master)",
    )
    startDate: dt.datetime = Field(
        ...,
        description="Start date of the education (YYYY-MM-DD)",
    )
    endDate: dt.datetime | None = Field(
        None,
        description="End date of the education (YYYY-MM-DD)",
    )
    score: str | None = Field(
        None,
        description="Score or grade achieved",
    )
    courses: list[str] = Field(
        default_factory=list,
        description="List of relevant courses taken",
    )


__EDUCATION_ITEM_EXAMPLE = {
    "institution": "University",
    "url": "https://institution.com/",
    "area": "Software Development",
    "studyType": "Bachelor",
    "startDate": "2011-01-01",
    "endDate": "2013-01-01",
    "score": "4.0",
    "courses": ["DB1101 - Basic SQL"],
}

assert EducationItem.model_validate(__EDUCATION_ITEM_EXAMPLE)  # noqa: S101
