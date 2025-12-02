"""
Schema for this part of the json resume:

```
    "profiles": [{
      "network": "Twitter",
      "username": "john",
      "url": "https://twitter.com/john"
    }]
```

"""

import typing as t

from pydantic import Field, HttpUrl

from ...schemas_utils import consolidate_id, sanitize_text
from .._abc import JsonResumeBaseModel


class Profile(JsonResumeBaseModel):
    network: str | None = Field(
        None,
        description="Name of the social network",
    )
    username: str | None = Field(
        None,
        description="Username on the social network",
    )
    url: HttpUrl | None = Field(
        None,
        description="URL to the profile on the social network",
    )

    @property
    def item_type(self) -> str:
        return "profiles"

    @t.override
    def get_id(self) -> str:
        return consolidate_id(
            self.item_type,
            sanitize_text(self.network) if self.network else "no_network",
            sanitize_text(self.username) if self.username else "no_username",
        )

    __EXAMPLE__: t.ClassVar = {
        "network": "Twitter",
        "username": "john",
        "url": "https://twitter.com/john",
    }
