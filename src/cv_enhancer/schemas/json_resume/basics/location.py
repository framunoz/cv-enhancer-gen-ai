"""
Schema for this part of the json resume:

```
    "location": {
      "address": "2712 Broadway St",
      "postalCode": "CA 94115",
      "city": "San Francisco",
      "countryCode": "US",
      "region": "California"
    },
```

"""

import typing as t

from pydantic import Field

from ...schemas_utils import consolidate_id, sanitize_text
from .._abc import JsonResumeBaseModel


class Location(JsonResumeBaseModel):
    address: str | None = Field(
        None,
        description="Street address",
    )
    postalCode: str | None = Field(
        None,
        description="Postal code",
    )
    city: str | None = Field(
        None,
        description="City name",
    )
    countryCode: str | None = Field(
        None,
        description="Country code (e.g., US)",
        min_length=2,
        max_length=3,
    )
    region: str | None = Field(
        None,
        description="Region or state",
    )

    @t.override
    def get_id(self) -> str:
        return consolidate_id(
            self.item_type,
            sanitize_text(self.postalCode) if self.postalCode else "no_postal_code",
        )

    @property
    def item_type(self) -> str:
        return "location"

    __EXAMPLE__: t.ClassVar = {
        "address": "2712 Broadway St",
        "postalCode": "CA 94115",
        "city": "San Francisco",
        "countryCode": "US",
        "region": "California",
    }
