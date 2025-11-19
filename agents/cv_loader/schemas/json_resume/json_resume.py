from pydantic import BaseModel, Field

from .awards import AwardItem
from .basics.basics import Basics
from .certificates import CertificateItem
from .education import EducationItem
from .publications import PublicationItem
from .volunteer import VolunteerItem
from .work import WorkItem


class JsonResume(BaseModel):
    """
    Schema for the JSON Resume format.

    See: https://jsonresume.org/schema/
    """

    basics: Basics = Field(
        ...,
        description="Basic information about the individual",
    )
    work: list[WorkItem] = Field(
        default_factory=list,
        description="List of work experiences",
    )
    volunteer: list[VolunteerItem] = Field(
        default_factory=list,
        description="List of volunteer experiences",
    )
    education: list[EducationItem] = Field(
        default_factory=list,
        description="List of educational qualifications",
    )
    awards: list[AwardItem] = Field(
        default_factory=list,
        description="List of awards received",
    )
    certificates: list[CertificateItem] = Field(
        default_factory=list,
        description="List of certificates obtained",
    )
    publications: list[PublicationItem] = Field(
        default_factory=list,
        description="List of publications",
    )


__JSON_RESUME_EXAMPLE = {
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
            "region": "California",
        },
        "profiles": [{
            "network": "Twitter",
            "username": "john",
            "url": "https://twitter.com/john",
        }],
    },
    "work": [
        {
            "name": "Company",
            "position": "President",
            "url": "https://company.com",
            "startDate": "2013-01-01",
            "endDate": "2014-01-01",
            "summary": "Description…",
            "highlights": ["Started the company"],
        },
        {
            "name": "Company 2",
            "position": "President",
            "url": "https://company.com",
            "startDate": "2013-01-01",
            "summary": "Description…",
            "highlights": ["Started the company"],
        },
    ],
    "volunteer": [{
        "organization": "Organization",
        "position": "Volunteer",
        "url": "https://organization.com/",
        "startDate": "2012-01-01",
        "endDate": "2013-01-01",
        "summary": "Description…",
        "highlights": ["Awarded 'Volunteer of the Month'"],
    }],
    "education": [{
        "institution": "University",
        "url": "https://institution.com/",
        "area": "Software Development",
        "studyType": "Bachelor",
        "startDate": "2011-01-01",
        "endDate": "2013-01-01",
        "score": "4.0",
        "courses": ["DB1101 - Basic SQL"],
    }],
    "awards": [{
        "title": "Award",
        "date": "2014-11-01",
        "awarder": "Company",
        "summary": "There is no spoon.",
    }],
    "certificates": [{
        "name": "Certificate",
        "date": "2021-11-07",
        "issuer": "Company",
        "url": "https://certificate.com",
    }],
    "publications": [{
        "name": "Publication",
        "publisher": "Company",
        "releaseDate": "2014-10-01",
        "url": "https://publication.com",
        "summary": "Description…",
    }],
    "skills": [{
        "name": "Web Development",
        "level": "Master",
        "keywords": ["HTML", "CSS", "JavaScript"],
    }],
    "languages": [{"language": "English", "fluency": "Native speaker"}],
    "interests": [{"name": "Wildlife", "keywords": ["Ferrets", "Unicorns"]}],
    "references": [{"name": "Jane Doe", "reference": "Reference…"}],
    "projects": [{
        "name": "Project",
        "startDate": "2019-01-01",
        "endDate": "2021-01-01",
        "description": "Description...",
        "highlights": ["Won award at AIHacks 2016"],
        "url": "https://project.com/",
    }],
}

assert JsonResume.model_validate(__JSON_RESUME_EXAMPLE)  # noqa: S101
