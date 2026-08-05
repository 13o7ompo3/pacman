"""A module for defining color palettes."""

from dataclasses import dataclass
from pygame import Color, Surface


@dataclass
class ColorPalette:
    """A color palette with six shades of a color.

    Attributes:
        darkest (Color): The darkest shade of the color.
        darker (Color): A darker shade of the color.
        dark (Color): A dark shade of the color.
        light (Color): A light shade of the color.
        lighter (Color): A lighter shade of the color.
        lightest (Color): The lightest shade of the color.

    """

    darkest: Color
    darker: Color
    dark: Color
    light: Color
    lighter: Color
    lightest: Color

    @classmethod
    def load_from_surface(cls, surface: Surface) -> "ColorPalette":
        """Load a color palette from a surface.

        Args:
            surface (Surface): The surface to load the color palette from.

        Returns:
            ColorPalette: The loaded color palette.

        """
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
