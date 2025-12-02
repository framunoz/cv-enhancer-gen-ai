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
    institution: str | None = Field(
        None,
        description="Name of the educational institution",
    )
    url: HttpUrl | t.Literal[""] | None = Field(
        None,
        description="URL of the educational institution",
    )
    area: str | None = Field(
        None,
        description="Area of study",
    )
    studyType: str | None = Field(
        None,
        description="Type of study (e.g., Bachelor, Master)",
    )
    startDate: dt.datetime | None = Field(
        None,
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
    courses: list[str] | None = Field(
        None,
        description="List of relevant courses taken",
    )

    @property
    def item_type(self) -> str:
        return "education"

    __EXAMPLE__ = {
        "institution": "University",
        "url": "https://institution.com/",
        "area": "Software Development",
        "studyType": "Bachelor",
        "startDate": "2011-01-01",
        "endDate": "2013-01-01",
        "score": "4.0",
        "courses": ["DB1101 - Basic SQL"],
    }


assert EducationItem.model_validate(EducationItem.__EXAMPLE__)  # noqa: S101
