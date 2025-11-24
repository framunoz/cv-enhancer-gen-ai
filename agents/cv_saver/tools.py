import logging
import os
from pathlib import Path

from .schemas import JsonResume

logger = logging.getLogger(__name__)


def save_cv_as_json(json_resume_str: str) -> None:
    """Saves the CV in JSON format to a file.

    Args:
        json_resume_str (str): The CV data in JSON format as a string.
    """
    json_resume = JsonResume.model_validate_json(json_resume_str)
    logger.debug("CV parsed successfully: %s", json_resume)

    file_path_str = os.environ.get("DB_PATH")

    if file_path_str is None:
        raise ValueError("DB_PATH environment variable is not set.")

    # Ensure the directory exists
    basics = json_resume.basics
    email = basics.email if basics and basics.email else "unknown"
    file_path = Path(file_path_str) / f"{email}_resume.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as json_file:
        json_file.write(json_resume.model_dump_json(indent=2, ensure_ascii=False))
