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

import datetime as dt
import typing as t

from pydantic import BaseModel, Field, HttpUrl

from ..schemas_utils import consolidate_id, sanitize_text


class CertificateItem(BaseModel):
    name: str | None = Field(
        None,
        description="Name of the certificate",
    )
    date: dt.datetime | None = Field(
        None,
        description="Date when the certificate was issued (YYYY-MM-DD)",
    )
    issuer: str | None = Field(
        None,
        description="Name of the organization or person who issued the certificate",
    )
    url: HttpUrl | t.Literal[""] | None = Field(
        None,
        description="URL to the certificate or related information",
    )
    summary: str | None = Field(
        None,
        description="Summary or description of the certificate",
    )
    keywords: list[str] | None = Field(
        None,
        description="List of keywords extracted from the certificate item",
    )

    __EXAMPLE__ = {
        "name": "Certificate",
        "date": "2021-11-07",
        "issuer": "Company",
        "url": "https://certificate.com",
        "summary": "This is to certify that...",
        "keywords": ["certification", "achievement"],
    }

    @property
    def item_type(self) -> str:
        return "certificate"

    def get_id(self) -> str:
        return consolidate_id(
            "certificate",
            sanitize_text(self.name or "no_name", max_len=10),
            sanitize_text(self.issuer or "no_issuer", max_len=10),
            self.date.strftime("%Y%m%d") if self.date else "no_date",
        )

    def format(self) -> str:
        return f"""
## Certificate: {self.name}

###  Issuer: {self.issuer}

- Summary:
    > {self.summary}

- Keywords: {', '.join(self.keywords) if self.keywords else 'N/A'}
"""


assert CertificateItem.model_validate(CertificateItem.__EXAMPLE__)  # noqa: S101
