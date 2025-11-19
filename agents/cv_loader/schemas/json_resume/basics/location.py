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


class Location(BaseModel):
    address: str = Field(
        ...,
        description="Street address",
        min_length=1,
    )
    postalCode: str = Field(
        ...,
        description="Postal code",
        min_length=1,
    )
    city: str = Field(
        ...,
        description="City name",
        min_length=1,
    )
    countryCode: str = Field(
        ...,
        description="Country code (e.g., US)",
        min_length=2,
        max_length=3,
    )
    region: str = Field(
        ...,
        description="Region or state",
        min_length=1,
    )
