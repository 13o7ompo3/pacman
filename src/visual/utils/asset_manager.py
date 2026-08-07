"""A module for managing game assets."""

from pathlib import Path
from typing import Iterator
from pygame import Surface, image
import pygame
from pygame.font import Font
import logging


logger = logging.getLogger(__name__)


class AssetManager:
    """A class for managing game assets.

    Attributes:
        _registered_images (dict): A dictionary of registered image paths.
        _loaded_images (dict): A dictionary of loaded image surfaces.
        _registered_fonts (dict): A dictionary of registered font paths.
        _loaded_fonts (dict): A dictionary of loaded font objects.
        _registered_audios (dict): A dictionary of registered audio paths.
        progress (int): The current progress of asset loading.

    """

    def __init__(self) -> None:
        """Initialize an AssetManager instance."""
        self._registered_images: dict[str, Path | str] = {}
        self._loaded_images: dict[str, Surface] = {}
        self._registered_fonts: dict[str, tuple[Path | str, int]] = {}
        self._loaded_fonts: dict[str, Font] = {}
        self._registered_audios: dict[str, Path | str] = {}
        # self._loaded_audios: dict[str, Surface] = {}
        self.progress: int = 0

    def register_image(self, key: str, path: Path | str) -> None:
        """Register an image asset.

        Args:
            key (str): The key to register the image under.
            path (Path | str): The path to the image file.

        """
        self._registered_images[key] = path

    def register_font(self, key: str, path: Path | str, size: int) -> None:
        """Register a font asset.

        Args:
            key (str): The key to register the font under.
            path (Path | str): The path to the font file.
            size (int): The size of the font.

        """
        self._registered_fonts[key] = (path, size)

    def register_audio(self, key: str, path: Path | str) -> None:
        """Register an audio asset.

        Args:
            key (str): The key to register the audio under.
            path (Path | str): The path to the audio file.

        """
        self._registered_audios[key] = path

    @property
    def total_assets(self) -> int:
        """Get the total number of registered assets.

        Returns:
            int: The total number of registered assets.

        """
        return (
            len(self._registered_images)
            + len(self._registered_fonts)
            + len(self._registered_audios)
        )

    @property
    def images(self) -> list[str]:
        """Get a list of registered image keys.

        Returns:
            list[str]: A list of registered image keys.

        """
        return list(self._loaded_images.keys())

    @property
    def fonts(self) -> list[str]:
        """Get a list of registered font keys.

        Returns:
            list[str]: A list of registered font keys.

        """
        return list(self._loaded_fonts.keys())

    def load(self) -> None:
        """Load all registered assets."""
        for _ in self.load_progress():
            pass

    def load_progress(self) -> Iterator[Path | str | Exception]:
        """Load all registered assets with progress tracking.

        Yields:
            Path | str | Exception: The path or key of the asset being loaded\
            or an exception if loading fails.

        """
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
            logger.info(
                f"{self.total_assets} assets have been successfully loaded"
            )
        except FileNotFoundError:
            yield Exception("File not found")
        except pygame.error as error:
            yield error
        except Exception:
            yield Exception("Could not load assets")

    def image(self, key: str) -> Surface:
        """Get a loaded image surface by key.

        Args:
            key (str): The key of the image to retrieve.

        """
        return self._loaded_images[key]

    def font(self, key: str) -> Font:
        """Get a loaded font object by key.

        Args:
            key (str): The key of the font to retrieve.

        """
        return self._loaded_fonts[key]
