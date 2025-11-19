from pydantic import BaseModel, Field


class JobOfferSummarized(BaseModel):
    job_description: str = Field(..., description="Concise description of the job")
    requirements: list[str] = Field(..., description="Key requirements listed clearly")
    tech_stack: list[str] = Field(..., description="Technologies and tools mentioned")

__SCHEMA_EXAMPLE = {
    "job_description": "Develop and maintain web applications.",
    "requirements": ["Python", "Django", "REST APIs"],
    "tech_stack": ["AWS", "Docker", "PostgreSQL"],
}

assert JobOfferSummarized(**__SCHEMA_EXAMPLE), "Example does not conform to schema"  # noqa: S101
