from dataclasses import dataclass
from pygame import Color, PixelArray, Surface


@dataclass
class ColorPalette:
    darkest: Color
    darker: Color
    dark: Color
    light: Color
    lighter: Color
    lightest: Color

    @classmethod
    def load_from_surface(cls, surface: Surface) -> "ColorPalette":
        darkest = surface.get_at((0, 0))
        darker = surface.get_at((1, 0))
        dark = surface.get_at((2, 0))
        light = surface.get_at((3, 0))
        lighter = surface.get_at((4, 0))
        lightest = surface.get_at((5, 0))

        return cls(
            darkest,
            darker,
            dark,
            light,
            lighter,
            lightest,
        )


DEFAULT_PALETTE = ColorPalette(
    Color("#272744"),
    Color("#494d7e"),
    Color("#8b6d9c"),
    Color("#c69fa5"),
    Color("#f2d3ab"),
    Color("#fbf5ef"),
)
