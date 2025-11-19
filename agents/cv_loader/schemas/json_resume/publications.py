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

import typing as t

from pydantic import BaseModel, Field, HttpUrl


class PublicationItem(BaseModel):
    name: str = Field(
        ...,
        description="Name of the publication",
    )
    publisher: str = Field(
        ...,
        description="Publisher of the publication",
    )
    releaseDate: str = Field(
        ...,
        description="Release date of the publication (YYYY-MM-DD)",
    )
    url: HttpUrl | t.Literal[""] = Field(
        ...,
        description="URL of the publication",
    )
    summary: str = Field(
        ...,
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
