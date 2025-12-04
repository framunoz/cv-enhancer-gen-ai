"""
Schema for this part of the json resume:

```
  "basics": {
    "name": "John Doe",
    "label": "Programmer",
    "image": "",
    "email": "john@gmail.com",
    "phone": "(912) 555-4321",
    "url": "https://johndoe.com",
    "summary": "A summary of John Doe…",
    "location": {
      "address": "2712 Broadway St",
      "postalCode": "CA 94115",
      "city": "San Francisco",
      "countryCode": "US",
      "region": "California"
    },
    "profiles": [{
      "network": "Twitter",
      "username": "john",
      "url": "https://twitter.com/john"
    }]
  },
```

"""

import typing as t

from pydantic import EmailStr, Field, HttpUrl

from ...schemas_utils import consolidate_id, sanitize_text
from .._abc import JsonResumeBaseModel
from .location import Location
from .profile import Profile


class Basics(JsonResumeBaseModel):
    name: str | None = Field(
        None,
        description="Full name of the individual",
    )
    label: str | None = Field(
        None,
        description="Professional title or label",
    )
    image: HttpUrl | t.Literal[""] | None = Field(
        None,
        description="URL to the individual's image",
    )
    email: EmailStr | None = Field(
        None,
        description="Email address",
    )
    phone: str | None = Field(
        None,
        description="Phone number",
    )
    url: HttpUrl | None = Field(
        None,
        description="Personal or professional website URL",
    )
    summary: str | None = Field(
        None,
        description="A brief summary about the individual",
    )
    location: Location | None = Field(
        None,
        description=(
            "Location details including address, postal code, city, country code, and"
            " region"
        ),
    )
    profiles: list[Profile] | None = Field(
        None,
        description=(
            "List of social media or professional profiles with network, username,"
            " and URL"
        ),
    )

    @t.override
    def get_id(self) -> str:
        return consolidate_id(
            self.item_type,
            sanitize_text(self.name) if self.name else "no_name",
        )

    @property
    def item_type(self) -> str:
        return "basics"

    __EXAMPLE__: t.ClassVar = {
        "name": "John Doe",
        "label": "Programmer",
        "image": "",
        "email": "john@gmail.com",
        "phone": "(912) 555-4321",
        "url": "https://johndoe.com",
        "summary": "A summary of John Doe…",
        "location": Location.__EXAMPLE__,
        "profiles": [Profile.__EXAMPLE__],
    }


assert Basics(**Basics.__EXAMPLE__), "Example does not conform to schema"  # noqa: S101
