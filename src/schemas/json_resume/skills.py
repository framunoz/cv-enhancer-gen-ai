"""
Schema for this part of the json resume:

```
  "skills": [{
    "name": "Web Development",
    "level": "Master",
    "keywords": [
      "HTML",
      "CSS",
      "JavaScript"
    ]
  }],
```
"""

from pydantic import BaseModel, Field


class SkillItemEssential(BaseModel):
    keywords: list[str] | None = Field(
        None,
        description="List of keywords related to the skill",
    )


class SkillItem(
    BaseModel,
):
    name: str | None = Field(
        None,
        description="Name of the skill",
    )
    level: str | None = Field(
        None,
        description="Proficiency level of the skill",
    )
    keywords: list[str] | None = Field(
        None,
        description="List of keywords related to the skill",
    )

    def get_essential(self) -> SkillItemEssential:
        return SkillItemEssential(
            keywords=self.keywords,
        )

    __EXAMPLE__ = {
        "name": "Web Development",
        "level": "Master",
        "keywords": [
            "HTML",
            "CSS",
            "JavaScript",
        ],
    }


assert SkillItem.model_validate(SkillItem.__EXAMPLE__)  # noqa: S101
