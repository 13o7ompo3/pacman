from pydantic import (
    BaseModel, ConfigDict, ValidationError,
    Field, model_validator, ValidatorFunctionWrapHandler, WrapValidator)
from pydantic_core import PydanticUseDefault
import json
import logging
from typing import List, Annotated, Any, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar('T')


def _use_default_on_error(value: Any,
                          handler: ValidatorFunctionWrapHandler) -> Any:
    try:
        return handler(value)
    except ValidationError:
        raise PydanticUseDefault()


type FallbackToDefault[T] = Annotated[T, WrapValidator(_use_default_on_error)]


class LevelConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    width: FallbackToDefault[int] = Field(default=10, ge=10, le=22)
    height: FallbackToDefault[int] = Field(default=10, ge=10, le=22)
    seed: FallbackToDefault[str | int] = Field(default=1337)
    level_max_time: FallbackToDefault[int] = Field(default=90, ge=10, le=120)
    speed: FallbackToDefault[float] = Field(default=75, ge=1, le=200)
    pacgum: FallbackToDefault[int] = Field(default=1337, ge=0)


class Config(BaseModel):
    model_config = ConfigDict(extra="ignore")

    levels: FallbackToDefault[List[LevelConfig]] = Field(
        default=[LevelConfig()])
    lives: FallbackToDefault[int] = Field(default=3, ge=1, le=5)
    points_per_pacgum: FallbackToDefault[int] = Field(default=10, ge=0, le=20)
    points_per_super_pacgum: FallbackToDefault[int] = Field(
        default=50, ge=0, le=100)
    points_per_ghost: FallbackToDefault[int] = Field(default=200, ge=0, le=400)
    super_pacgum_duration: FallbackToDefault[int] = Field(
        default=500, ge=200, le=1000)

    @model_validator(mode="after")
    def validator(self) -> "Config":
        default_levels = [LevelConfig(width=10, height=10, seed=1337,
                                      level_max_time=90, speed=75,
                                      pacgum=1337),
                          LevelConfig(width=11, height=11, seed=42,
                                      level_max_time=95, speed=75,
                                      pacgum=1337),
                          LevelConfig(width=13, height=12, seed=1337,
                                      level_max_time=100, speed=80,
                                      pacgum=1337),
                          LevelConfig(width=13, height=15, seed=42,
                                      level_max_time=105, speed=80,
                                      pacgum=1337),
                          LevelConfig(width=15, height=15, seed=1337,
                                      level_max_time=110, speed=85,
                                      pacgum=1337),
                          LevelConfig(width=17, height=15, seed=42,
                                      level_max_time=115, speed=90,
                                      pacgum=1337),
                          LevelConfig(width=17, height=17, seed=1337,
                                      level_max_time=120, speed=95,
                                      pacgum=1337),
                          LevelConfig(width=17, height=19, seed=42,
                                      level_max_time=120, speed=100,
                                      pacgum=1337),
                          LevelConfig(width=19, height=19, seed=1337,
                                      level_max_time=120, speed=105,
                                      pacgum=1337),
                          LevelConfig(width=20, height=20, seed=42,
                                      level_max_time=120, speed=110,
                                      pacgum=1337)]
        self.levels = self.levels + default_levels[len(self.levels):]
        return self


def _strip_comments(content: str) -> str:
    return '\n'.join(line.split('#')[0].rstrip()
                     for line in content.splitlines()
                     if line.split('#')[0].rstrip())


def parse_config(config_file: str) -> Config:
    try:
        with open(config_file, 'r') as f:
            raw_content = f.read()
    except UnicodeDecodeError as e:
        logger.error(f"Decode error '{config_file}': {e}."
                     " Proceeding with safe defaults.")
        return Config()
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
        logger.error(
            f"Validation error in '{config_file}': {e}."
            " Proceeding with safe defaults."
        )
        return Config()

