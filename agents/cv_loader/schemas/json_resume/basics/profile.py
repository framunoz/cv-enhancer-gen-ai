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

from pydantic import BaseModel, Field, HttpUrl


class Profile(BaseModel):
    network: str = Field(
        ...,
        description="Name of the social network",
        min_length=1,
    )
    username: str = Field(
        ...,
        description="Username on the social network",
        min_length=1,
    )
    url: HttpUrl = Field(
        ...,
        description="URL to the profile on the social network",
    )
