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


def _yield_if_exists(
    item: JsonResumeBaseModel | t.Iterable[JsonResumeBaseModel] | None,
) -> t.Generator[JsonResumeBaseModel]:
    if item is not None:
        if isinstance(item, JsonResumeBaseModel):
            yield item
        else:
            yield from item


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

    def iter_items(self) -> t.Generator[JsonResumeBaseModel]:
        """Iterate over all items in the JSON Resume."""

        if basics := self.basics:
            yield from _yield_if_exists(basics)
            yield from _yield_if_exists(basics.location)
            yield from _yield_if_exists(basics.profiles)

        yield from _yield_if_exists(self.work)
        yield from _yield_if_exists(self.volunteer)
        yield from _yield_if_exists(self.education)
        yield from _yield_if_exists(self.awards)
        yield from _yield_if_exists(self.certificates)
        yield from _yield_if_exists(self.publications)
        yield from _yield_if_exists(self.skills)
        yield from _yield_if_exists(self.languages)
        yield from _yield_if_exists(self.interests)
        yield from _yield_if_exists(self.references)
        yield from _yield_if_exists(self.projects)

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
