from pydantic import BaseModel, ConfigDict, ValidationError, Field
import json
import logging
from typing import List

logger = logging.getLogger(__name__)


class LevelConfig(BaseModel):
    width: int = Field(default=28, ge=10)
    height: int = Field(default=31, ge=10)
    seed: str | int = Field(default=1337)


class Config(BaseModel):
    model_config = ConfigDict(extra="ignore")

    highscore_filename: str = "highscores.json"
    level: List[LevelConfig] = Field(default_factory=lambda: [LevelConfig()])
    lives: int = Field(default=3, ge=1)
    pacgum: int = Field(default=42, ge=0)
    points_per_pacgum: int = Field(default=10, ge=0)
    points_per_super_pacgum: int = Field(default=50, ge=0)
    points_per_ghost: int = Field(default=200, ge=0)
    seed: int = Field(default=42)
    level_max_time: int = Field(default=90, ge=10)


def _strip_comments(content: str) -> str:
    return '\n'.join(line.split('#')[0].rstrip()
                     for line in content.splitlines()
                     if line.split('#')[0].rstrip())


def parse_config(config_file: str) -> Config:
    try:
        with open(config_file, 'r') as f:
            raw_content = f.read()
    except OSError as e:
        logger.error(f"File error '{config_file}': {e}."
                     " Proceeding with safe defaults.")
        return Config()

    cleaned_content = _strip_comments(raw_content)

    try:
        config_data = json.loads(cleaned_content)
        if not isinstance(config_data, dict):
            raise ValueError("JSON root must be a dictionary.")
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Parse error in '{config_file}': {e}."
                     " Proceeding with safe defaults.")
        return Config()

    try:
        return Config(**config_data)
    except ValidationError as e:
        logger.warning("Invalid configuration values detected. "
                       "Clamping to defaults.")
        safe_data = config_data.copy()
        for error in e.errors():
            if len(error['loc']) > 0:
                bad_key = error['loc'][0]
                safe_data.pop(bad_key, None)

        try:
            return Config(**safe_data)
        except ValidationError:
            logger.error("Critical validation failure. "
                         "Proceeding with safe defaults.")
            return Config()
