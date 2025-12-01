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

from ..schemas_utils import consolidate_id, sanitize_text


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

    @property
    def item_type(self) -> str:
        return "skills"

    __EXAMPLE__ = {
        "name": "Web Development",
        "level": "Master",
        "keywords": [
            "HTML",
            "CSS",
            "JavaScript",
        ],
    }

    def get_id(self) -> str:
        return consolidate_id(
            "skill",
            sanitize_text(self.name or "no_skill", max_len=15),
        )

    def format(self) -> str:
        return f"""
## Skill: {self.name}

- Level: {self.level}

- Keywords: {', '.join(self.keywords) if self.keywords else 'N/A'}
"""


assert SkillItem.model_validate(SkillItem.__EXAMPLE__)  # noqa: S101
