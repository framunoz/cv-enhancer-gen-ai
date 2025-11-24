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

from pydantic import BaseModel, Field


class LocationEssential(BaseModel):
    pass


class Location(BaseModel):
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

    def get_essential(self) -> LocationEssential:
        return LocationEssential()

    __EXAMPLE__ = {
        "address": "2712 Broadway St",
        "postalCode": "CA 94115",
        "city": "San Francisco",
        "countryCode": "US",
        "region": "California",
    }
