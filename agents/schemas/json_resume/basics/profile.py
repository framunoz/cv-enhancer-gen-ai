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


class ProfileEssential(BaseModel):
    pass


class Profile(BaseModel):
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

    def get_essential(self) -> ProfileEssential:
        return ProfileEssential()

    __EXAMPLE__ = {
        "network": "Twitter",
        "username": "john",
        "url": "https://twitter.com/john",
    }
