import json
import logging
from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    model_validator,
)

logger = logging.getLogger(__name__)


class LevelConfig(BaseModel):
    """Configuration for a single level in the game."""

    model_config = ConfigDict(extra="ignore")

    width: int = Field(default=10, ge=10, le=22)
    height: int = Field(default=10, ge=10, le=22)
    seed: int = Field(default=1337)
    level_max_time: int = Field(default=90, ge=10, le=120)
    speed: float = Field(default=75, ge=1, le=200)


def default_handler(value: Any, arg: str) -> Any:
    """Handle defualt clamping with clear messages.

    Args:
        value (Any): the default value.
        arg (str): the argument name to be set to default.

    Returns:
        Any: the default factory.
    """

    def inner() -> Any:
        """Inner function to be returned."""
        logger.warning(f"{arg} was missing and clamped to default ({value})")
        return value

    return inner


class Config(BaseModel):
    """Configuration for the game."""

    model_config = ConfigDict(extra="ignore")

    levels: list[LevelConfig] = Field(default_factory=list)
    lives: int = Field(default_factory=default_handler(3, "lives"), ge=1, le=5)
    points_per_pacgum: int = Field(
        default_factory=default_handler(10, "points_per_pacgum"), ge=0, le=20
    )
    points_per_super_pacgum: int = Field(
        default_factory=default_handler(50, "points_per_super_pacgum"),
        ge=0,
        le=100,
    )
    points_per_ghost: int = Field(
        default_factory=default_handler(200, "points_per_ghost"), ge=0, le=400
    )
    super_pacgum_duration: int = Field(
        default_factory=default_handler(10, "super_pacgum_duration"),
        ge=1,
        le=30,
    )

    @model_validator(mode="after")
    def validator(self) -> "Config":
        """Validator to ensure that the levels list is populated defaults.

        Returns:
            Config: The validated configuration.
        """
        default_levels = [
            LevelConfig(
                width=10,
                height=10,
                seed=1337,
                level_max_time=90,
                speed=75,
            ),
            LevelConfig(
                width=11,
                height=11,
                seed=42,
                level_max_time=95,
                speed=75,
            ),
            LevelConfig(
                width=13,
                height=12,
                seed=1337,
                level_max_time=100,
                speed=80,
            ),
            LevelConfig(
                width=13,
                height=15,
                seed=42,
                level_max_time=105,
                speed=80,
            ),
            LevelConfig(
                width=15,
                height=15,
                seed=1337,
                level_max_time=110,
                speed=85,
            ),
            LevelConfig(
                width=17,
                height=15,
                seed=42,
                level_max_time=115,
                speed=90,
            ),
            LevelConfig(
                width=17,
                height=17,
                seed=1337,
                level_max_time=120,
                speed=95,
            ),
            LevelConfig(
                width=17,
                height=19,
                seed=42,
                level_max_time=120,
                speed=100,
            ),
            LevelConfig(
                width=19,
                height=19,
                seed=1337,
                level_max_time=120,
                speed=105,
            ),
            LevelConfig(
                width=20,
                height=20,
                seed=42,
                level_max_time=120,
                speed=110,
            ),
        ]
        level_len = len(self.levels)
        if level_len < 10:
            logger.warning(
                f"{level_len} levels were provided by config the rest"
                f" {10 - level_len} were clamped to safe defaults"
            )
        self.levels = self.levels + default_levels[len(self.levels):]
        return self


def _strip_comments(content: str) -> str:
    """Strip comments from the given content.

    Args:
        content (str): The content to strip comments from.

    Returns:
        str: The content with comments removed.
    """
    return "\n".join(
        line
        for line in content.splitlines()
        if not line.strip().startswith("#")
    )


def parse_config(config_file: str) -> Config:
    """Parse the configuration file and return a Config object.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        Config: The parsed configuration object.
    """
    config_path = Path(config_file)
    if not config_path.is_file():
        logger.error("Config is not a file. resorting to defaults.")
        return Config()
    try:
        with open(config_path, "r") as f:
            raw_content = f.read()
    except OSError as e:
        logger.error(
            f"File error '{config_file}': {e}. Proceeding with safe defaults."
        )
        return Config()
    except Exception as e:
        logger.error(
            f"Unexpected error '{config_file}': {e}."
            " Proceeding with safe defaults."
        )
        return Config()

    cleaned_content = _strip_comments(raw_content)

    try:
        config_data = json.loads(cleaned_content)
        if not isinstance(config_data, dict):
            raise ValueError("JSON root must be a dictionary.")
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(
            f"Parse error in '{config_file}': {e}."
            " Proceeding with safe defaults."
        )
        return Config()
    except Exception as e:
        logger.error(
            f"Unexpected error '{config_file}': {e}."
            " Proceeding with safe defaults."
        )
        return Config()

    try:
        return Config(**config_data)
    except ValidationError as e:
        logger.error(
            f"Validation error in '{config_file}': {e}."
            " Proceeding with safe defaults."
        )
        return Config()
    except Exception as e:
        logger.error(
            f"Unexpected error '{config_file}': {e}."
            " Proceeding with safe defaults."
        )
        return Config()
