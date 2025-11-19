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
