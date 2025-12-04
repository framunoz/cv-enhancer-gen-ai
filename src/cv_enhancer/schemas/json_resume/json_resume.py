import typing as t

from pydantic import BaseModel, Field

from ._abc import JsonResumeBaseModel, JsonResumeFormattableBaseModel
from .awards import AwardItem
from .basics import Basics
from .certificates import CertificateItem
from .education import EducationItem
from .interests import InterestItem
from .languages import LanguageItem
from .projects import ProjectItem
from .publications import PublicationItem
from .references import ReferenceItem
from .skills import SkillItem
from .volunteer import VolunteerItem
from .work import WorkItem


class JsonResume(BaseModel):
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

    def iter_items(self) -> t.Generator[JsonResumeBaseModel]:  # noqa: PLR0912
        """Iterate over all items in the JSON Resume."""

        if basics := self.basics:
            yield basics

            if location := basics.location:
                yield location

            if profiles := basics.profiles:
                yield from profiles

        if work := self.work:
            yield from work

        if volunteer := self.volunteer:
            yield from volunteer

        if education := self.education:
            yield from education

        if awards := self.awards:
            yield from awards

        if certificates := self.certificates:
            yield from certificates

        if publications := self.publications:
            yield from publications

        if skills := self.skills:
            yield from skills

        if languages := self.languages:
            yield from languages

        if interests := self.interests:
            yield from interests

        if references := self.references:
            yield from references

        if projects := self.projects:
            yield from projects

    def iter_over_formatables(self) -> t.Generator[JsonResumeFormattableBaseModel]:
        """Iterate over all formattable items in the JSON Resume."""
        for item in self.iter_items():
            if isinstance(item, JsonResumeFormattableBaseModel):
                yield item

    def find_experience(self, exp_id: str) -> JsonResumeBaseModel | None:
        """Find an experience item by its ID."""
        for item in self.iter_items():
            if item.get_id() == exp_id:
                return item
        return None

    @property
    def item_type(self) -> str:
        return "json_resume"

    __EXAMPLE__: t.ClassVar = {
        "basics": Basics.__EXAMPLE__,
        "work": [WorkItem.__EXAMPLE__],
        "volunteer": [VolunteerItem.__EXAMPLE__],
        "education": [EducationItem.__EXAMPLE__],
        "awards": [AwardItem.__EXAMPLE__],
        "certificates": [CertificateItem.__EXAMPLE__],
        "publications": [PublicationItem.__EXAMPLE__],
        "skills": [SkillItem.__EXAMPLE__],
        "languages": [LanguageItem.__EXAMPLE__],
        "interests": [InterestItem.__EXAMPLE__],
        "references": [ReferenceItem.__EXAMPLE__],
        "projects": [ProjectItem.__EXAMPLE__],
    }


assert JsonResume.model_validate(JsonResume.__EXAMPLE__)  # noqa: S101
