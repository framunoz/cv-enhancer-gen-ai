"""
Schema for this part of the json resume:

```
  "publications": [{
    "name": "Publication",
    "publisher": "Company",
    "releaseDate": "2014-10-01",
    "url": "https://publication.com",
    "summary": "Description…"
  }],
```
"""

import datetime as dt
import typing as t

from pydantic import Field, HttpUrl

from ..schemas_utils import consolidate_id, sanitize_text
from ._abc import JsonResumeFormattableBaseModel


class PublicationItem(JsonResumeFormattableBaseModel):
    name: str | None = Field(
        None,
        description="Name of the publication",
    )
    publisher: str | None = Field(
        None,
        description="Publisher of the publication",
    )
    releaseDate: dt.datetime | None = Field(
        None,
        description="Release date of the publication (YYYY-MM-DD)",
    )
    url: HttpUrl | t.Literal[""] | None = Field(
        None,
        description="URL of the publication",
    )
    summary: str | None = Field(
        None,
        description="Summary of the publication",
    )

    @property
    def item_type(self) -> str:
        return "publications"

    __EXAMPLE__: t.ClassVar = {
        "name": "Publication",
        "publisher": "Company",
        "releaseDate": "2014-10-01",
        "url": "https://publication.com",
        "summary": "Description…",
    }

    @t.override
    def get_id(self) -> str:
        return consolidate_id(
            self.item_type,
            self.releaseDate.strftime("%Y%m%d") if self.releaseDate else "no_date",
            sanitize_text(self.name or "no_name"),
            sanitize_text(self.publisher or "no_publisher"),
        )

    @t.override
    def format(self) -> str:
        return (
            f"Publication: {self.name}\n"
            f"Publisher: {self.publisher}\n"
            f"Release Date: {self.releaseDate.date() if self.releaseDate else 'N/A'}\n"
            f"URL: {self.url}\n"
            f"Summary: {self.summary}\n"
        )


assert PublicationItem.model_validate(PublicationItem.__EXAMPLE__)  # noqa: S101
