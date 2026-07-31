from pathlib import Path
import time
from typing import Iterator
from pygame import Surface, image
import pygame
from pygame.font import Font


class AssetManager:
    def __init__(self) -> None:
        self._registered_images: dict[str, Path | str] = {}
        self._loaded_images: dict[str, Surface] = {}
        self._registered_fonts: dict[str, tuple[Path | str, int]] = {}
        self._loaded_fonts: dict[str, Font] = {}
        self._registered_audios: dict[str, Path | str] = {}
        # self._loaded_audios: dict[str, Surface] = {}
        self.progress: int = 0

    def register_image(self, key: str, path: Path | str) -> None:
        self._registered_images[key] = path

    def register_font(self, key: str, path: Path | str, size: int) -> None:
        self._registered_fonts[key] = (path, size)

    def register_audio(self, key: str, path: Path | str) -> None:
        self._registered_audios[key] = path

    @property
    def total_assets(self) -> int:
        return (
            len(self._registered_images)
            + len(self._registered_fonts)
            + len(self._registered_audios)
        )

    @property
    def images(self) -> list[str]:
        return list(self._loaded_images.keys())

    @property
    def fonts(self) -> list[str]:
        return list(self._loaded_fonts.keys())

    def load(self) -> None:
        for _ in self.load_progress():
            pass

    def load_progress(self) -> Iterator[Path | str | Exception]:
        try:
            # load images
            for key, path in self._registered_images.copy().items():
                del self._registered_images[key]
                self._loaded_images[key] = image.load(path).convert_alpha()
                yield key
            # load fonts
            for key, (path, size) in self._registered_fonts.copy().items():
                del self._registered_fonts[key]
                self._loaded_fonts[key] = Font(path, size)
                yield key
        except FileNotFoundError:
            yield Exception("File not found")
        except pygame.error as error:
            yield error
        except Exception:
            yield Exception("Could not load assets")

    def image(self, key: str) -> Surface:
        return self._loaded_images[key]

    def font(self, key: str) -> Font:
        return self._loaded_fonts[key]
