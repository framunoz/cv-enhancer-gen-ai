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

from pydantic import BaseModel, Field, HttpUrl


class PublicationItem(BaseModel):
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


__PUBLICATION_ITEM_EXAMPLE = {
    "name": "Publication",
    "publisher": "Company",
    "releaseDate": "2014-10-01",
    "url": "https://publication.com",
    "summary": "Description…",
}

assert PublicationItem.model_validate(__PUBLICATION_ITEM_EXAMPLE)  # noqa: S101
