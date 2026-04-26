from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent


generic_settings_config_dict = SettingsConfigDict(
    env_nested_delimiter="_",
    extra="ignore",
    env_file=".env",
    env_file_encoding="utf-8",
)


class GoogleSettings(BaseSettings):
    api_key: str

    model_config = SettingsConfigDict(
        generic_settings_config_dict,
        env_prefix="GOOGLE_",
    )


class ChromadbSettings(BaseSettings):
    persist_dir: Path = PROJECT_ROOT / "db"

    model_config = SettingsConfigDict(
        generic_settings_config_dict,
        env_prefix="CHROMADB_",
    )


class JsonResumeSettings(BaseSettings):
    path: Path = PROJECT_ROOT / "data" / "json_resume_example.json"

    model_config = SettingsConfigDict(
        generic_settings_config_dict,
        env_prefix="JSON_RESUME_",
    )


class Settings(BaseSettings):
    google: GoogleSettings = GoogleSettings()
    chromadb: ChromadbSettings = ChromadbSettings()
    json_resume: JsonResumeSettings = JsonResumeSettings()
