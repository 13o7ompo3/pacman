import pygame
from pygame import Color, Surface

from src.visual.utils.image import Image


class Font:
    """A class for rendering text using a bitmap font."""

    def __init__(
        self, font_atlas: Surface, char_size: tuple[int, int]
    ) -> None:
        """Initialize the font with a font atlas and character size.

        Args:
            font_atlas (Surface): The surface containing the font atlas.
            char_size (tuple[int, int]): The size of each character.
        """
        chars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars += "[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        char_images = Image.split_surface(font_atlas, 6, 18)
        self.__char_mapping = {
            char: image for char, image in zip(chars, char_images)
        }
        self.__char_size = char_size

    def render(
        self, text: str, _: bool, color: Color, scale: int = 1
    ) -> Surface:
        """Render the given text using the bitmap font.

        Args:
            text (str): The text to render.
            _: bool: Unused parameter, kept for compatibility.
            color (Color): The color to apply to the rendered text.
            scale (int): text scale

        Returns:
            Surface: A surface containing the rendered text.
        """
        result = Surface(
            self.size(text),
            flags=pygame.SRCALPHA,
        )
        x, y = 0, 0
        for char in text:
            char_img = self.__char_mapping.get(char)
            if char_img:
                result.blit(char_img, (x, y))
                x += self.__char_size[0]
        Image.fill(result, color)
        if scale > 1:
            return Image.scale(result, scale)
        return result

    def size(self, text: str) -> tuple[int, int]:
        """Calculate the size of the rendered text.

        Args:
            text (str): The text to calculate the size for.

        Returns:
            tuple[int, int]: The width and height of the rendered text.
        """
        return (
            self.__char_size[0]
            * len([char for char in text if char in self.__char_mapping]),
            self.__char_size[1],
        )
