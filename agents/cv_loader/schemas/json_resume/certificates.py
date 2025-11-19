"""
Schema for this part of the json resume:

```
  "certificates": [{
    "name": "Certificate",
    "date": "2021-11-07",
    "issuer": "Company",
    "url": "https://certificate.com"
  }],
```
"""

import typing as t

from pydantic import BaseModel, Field, HttpUrl


class CertificateItem(BaseModel):
    name: str = Field(
        ...,
        description="Name of the certificate",
    )
    date: str = Field(
        ...,
        description="Date when the certificate was issued (YYYY-MM-DD)",
    )
    issuer: str = Field(
        ...,
        description="Name of the organization or person who issued the certificate",
    )
    url: HttpUrl | t.Literal[""] = Field(
        ...,
        description="URL to the certificate or related information",
    )


__CERTIFICATE_ITEM_EXAMPLE = {
    "name": "Certificate",
    "date": "2021-11-07",
    "issuer": "Company",
    "url": "https://certificate.com",
}

assert CertificateItem.model_validate(__CERTIFICATE_ITEM_EXAMPLE)  # noqa: S101
