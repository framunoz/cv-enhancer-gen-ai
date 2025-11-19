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


class SkillItem(BaseModel):
    name: str = Field(
        ...,
        description="Name of the skill",
    )
    level: str = Field(
        ...,
        description="Proficiency level of the skill",
    )
    keywords: list[str] = Field(
        default_factory=list,
        description="List of keywords related to the skill",
    )


__SKILL_ITEM_EXAMPLE = {
    "name": "Web Development",
    "level": "Master",
    "keywords": [
        "HTML",
        "CSS",
        "JavaScript",
    ],
}

assert SkillItem.model_validate(__SKILL_ITEM_EXAMPLE)  # noqa: S101
