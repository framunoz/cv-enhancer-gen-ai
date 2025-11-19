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

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from .location import Location
from .profile import Profile


class Basics(BaseModel):
    name: str = Field(
        ...,
        description="Full name of the individual",
        min_length=1,
    )
    label: str = Field(
        ...,
        description="Professional title or label",
        min_length=1,
    )
    image: HttpUrl | t.Literal[""] = Field(
        ...,
        description="URL to the individual's image",
    )
    email: EmailStr = Field(
        ...,
        description="Email address",
    )
    phone: str = Field(
        ...,
        description="Phone number",
        min_length=1,
    )
    url: HttpUrl = Field(
        ...,
        description="Personal or professional website URL",
    )
    summary: str = Field(
        ...,
        description="A brief summary about the individual",
        min_length=1,
    )
    location: Location = Field(
        ...,
        description=(
            "Location details including address, postal code, city, country code, and"
            " region"
        ),
    )
    profiles: list[Profile] = Field(
        default_factory=list,
        description=(
            "List of social media or professional profiles with network, username,"
            " and URL"
        ),
    )


__BASICS_SCHEMA_EXAMPLE = {
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
        "region": "California",
    },
    "profiles": [{
        "network": "Twitter",
        "username": "john",
        "url": "https://twitter.com/john",
    }],
}

assert Basics(  # noqa: S101
    **__BASICS_SCHEMA_EXAMPLE
), "Example does not conform to schema"
