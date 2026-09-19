from pygame import Color, Surface
import pygame

from src.visual.utils.image import Image


class Font:
    def __init__(
        self, font_atlas: Surface, char_size: tuple[int, int]
    ) -> None:
        chars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        char_images = Image.split_surface(font_atlas, 6, 18)
        self.__char_mapping = {
            char: image for char, image in zip(chars, char_images)
        }
        self.__char_size = char_size

    def render(self, text: str, _: bool, color: Color) -> Surface:
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
        return result

    def size(self, text: str) -> tuple[int, int]:
        return (
            self.__char_size[0]
            * len([char for char in text if char in self.__char_mapping]),
            self.__char_size[1],
        )
