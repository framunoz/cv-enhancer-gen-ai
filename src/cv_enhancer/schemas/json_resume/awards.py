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
import typing as t

from pydantic import Field

from ..schemas_utils import consolidate_id, sanitize_text
from ._abc import JsonResumeFormattableBaseModel


class AwardItem(JsonResumeFormattableBaseModel):
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

    __EXAMPLE__: t.ClassVar = {
        "title": "Award",
        "date": "2014-11-01",
        "awarder": "Company",
        "summary": "There is no spoon.",
    }

    @property
    def item_type(self) -> str:
        return "awards"

    @t.override
    def get_id(self) -> str:
        return consolidate_id(
            self.item_type,
            self.date.strftime("%Y%m%d") if self.date else "no_date",
            sanitize_text(self.title) if self.title else "no_title",
        )

    @t.override
    def format(self) -> str:
        return (
            f"Award: {self.title}\n"
            f"Date: {self.date.date() if self.date else 'N/A'}\n"
            f"Awarder: {self.awarder}\n"
            f"Summary: {self.summary}\n"
        )


assert AwardItem.model_validate(AwardItem.__EXAMPLE__)  # noqa: S101
