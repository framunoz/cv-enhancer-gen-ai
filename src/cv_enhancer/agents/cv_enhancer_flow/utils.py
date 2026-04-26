import logging

from cv_enhancer.schemas.json_resume import JsonResume

from .settings import Settings


def get_json_resume() -> JsonResume:
    """Load a JSON resume from a file and validate it against the JsonResume schema.

    Returns:
        JsonResume: The validated JSON resume object.
    """
    resume_path = Settings().json_resume.path

    if not resume_path.exists():
        # Fallback or error handling
        # For now, let's assume it exists or use a placeholder
        logging.warning(f"Resume file not found at {resume_path}. Using empty resume.")
        return JsonResume()

    with resume_path.open(encoding="utf-8") as f:
        json_resume = JsonResume.model_validate_json(f.read())

    return json_resume
