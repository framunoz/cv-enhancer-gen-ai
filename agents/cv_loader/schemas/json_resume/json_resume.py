from pydantic import BaseModel, Field

from .basics import Basics
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
