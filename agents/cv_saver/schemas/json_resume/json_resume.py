import typing as t

from pydantic import BaseModel, Field

from .awards import AwardItem, AwardItemEssential
from .basics import Basics, BasicsEssential
from .certificates import CertificateItem, CertificateItemEssential
from .education import EducationItem, EducationItemEssential
from .interests import InterestItem, InterestItemEssential
from .interface_essential import InterfaceEssential
from .languages import LanguageItem, LanguageItemEssential
from .projects import ProjectItem, ProjectItemEssential
from .publications import PublicationItem, PublicationItemEssential
from .references import ReferenceItem, ReferenceItemEssential
from .skills import SkillItem, SkillItemEssential
from .volunteer import VolunteerItem, VolunteerItemEssential
from .work import WorkItem, WorkItemEssential


class JsonResumeEssential(BaseModel):

    basics: BasicsEssential | None = Field(
        None,
        description="Basic information about the individual",
    )
    work: list[WorkItemEssential] | None = Field(
        None,
        description="List of work experiences",
    )
    volunteer: list[VolunteerItemEssential] | None = Field(
        None,
        description="List of volunteer experiences",
    )
    education: list[EducationItemEssential] | None = Field(
        None,
        description="List of educational qualifications",
    )
    awards: list[AwardItemEssential] | None = Field(
        None,
        description="List of awards received",
    )
    certificates: list[CertificateItemEssential] | None = Field(
        None,
        description="List of certificates obtained",
    )
    publications: list[PublicationItemEssential] | None = Field(
        None,
        description="List of publications",
    )
    skills: list[SkillItemEssential] | None = Field(
        None,
        description="List of skills",
    )
    languages: list[LanguageItemEssential] | None = Field(
        None,
        description="List of languages known",
    )
    interests: list[InterestItemEssential] | None = Field(
        None,
        description="List of interests",
    )
    references: list[ReferenceItemEssential] | None = Field(
        None,
        description="List of references",
    )
    projects: list[ProjectItemEssential] | None = Field(
        None,
        description="List of projects",
    )


class JsonResume(
    BaseModel,
):
    """
    Schema for the JSON Resume format.

    See: https://jsonresume.org/schema/
    """

    basics: Basics | None = Field(
        None,
        description="Basic information about the individual",
    )
    work: list[WorkItem] | None = Field(
        None,
        description="List of work experiences",
    )
    volunteer: list[VolunteerItem] | None = Field(
        None,
        description="List of volunteer experiences",
    )
    education: list[EducationItem] | None = Field(
        None,
        description="List of educational qualifications",
    )
    awards: list[AwardItem] | None = Field(
        None,
        description="List of awards received",
    )
    certificates: list[CertificateItem] | None = Field(
        None,
        description="List of certificates obtained",
    )
    publications: list[PublicationItem] | None = Field(
        None,
        description="List of publications",
    )
    skills: list[SkillItem] | None = Field(
        None,
        description="List of skills",
    )
    languages: list[LanguageItem] | None = Field(
        None,
        description="List of languages known",
    )
    interests: list[InterestItem] | None = Field(
        None,
        description="List of interests",
    )
    references: list[ReferenceItem] | None = Field(
        None,
        description="List of references",
    )
    projects: list[ProjectItem] | None = Field(
        None,
        description="List of projects",
    )

    def get_essential(self) -> JsonResumeEssential:
        def _get_essential_list(
            list_items: t.Sequence[InterfaceEssential] | None,
        ) -> list[BaseModel] | None:
            if list_items is None or len(list_items) == 0:
                return None
            list_essential_items = []
            for item in list_items:
                item_essential = item.get_essential()
                if len(item_essential.model_dump(exclude_none=True)) > 0:
                    list_essential_items.append(item_essential)
            return list_essential_items if len(list_essential_items) > 0 else None

        return JsonResumeEssential(
            basics=self.basics.get_essential() if self.basics else None,
            work=_get_essential_list(self.work),
            volunteer=_get_essential_list(self.volunteer),
            education=_get_essential_list(self.education),
            awards=_get_essential_list(self.awards),
            certificates=_get_essential_list(self.certificates),
            publications=_get_essential_list(self.publications),
            skills=_get_essential_list(self.skills),
            languages=_get_essential_list(self.languages),
            interests=_get_essential_list(self.interests),
            references=_get_essential_list(self.references),
            projects=_get_essential_list(self.projects),
        )

    __EXAMPLE__ = {
        "basics": {
            "name": "John Doe",
            "label": "Programmer",
            "image": "",
            "email": "john@gmail.com",
            "phone": "(912) 555-4321",
            "url": "https://johndoe.com",
            "summary": "A summary of John Doe...",
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
                "summary": "Description...",
                "highlights": ["Started the company"],
            },
            {
                "name": "Company 2",
                "position": "President",
                "url": "https://company.com",
                "startDate": "2013-01-01",
                "summary": "Description...",
                "highlights": ["Started the company"],
            },
        ],
        "volunteer": [{
            "organization": "Organization",
            "position": "Volunteer",
            "url": "https://organization.com/",
            "startDate": "2012-01-01",
            "endDate": "2013-01-01",
            "summary": "Description...",
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
            "summary": "Description...",
        }],
        "skills": [{
            "name": "Web Development",
            "level": "Master",
            "keywords": ["HTML", "CSS", "JavaScript"],
        }],
        "languages": [{"language": "English", "fluency": "Native speaker"}],
        "interests": [{"name": "Wildlife", "keywords": ["Ferrets", "Unicorns"]}],
        "references": [{"name": "Jane Doe", "reference": "Reference..."}],
        "projects": [{
            "name": "Project",
            "startDate": "2019-01-01",
            "endDate": "2021-01-01",
            "description": "Description...",
            "highlights": ["Won award at AIHacks 2016"],
            "url": "https://project.com/",
        }],
    }


assert JsonResume.model_validate(JsonResume.__EXAMPLE__)  # noqa: S101
