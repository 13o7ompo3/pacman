from dataclasses import dataclass
from pygame import Color


@dataclass(frozen=True)
class ColorPalette:
    darkest: Color
    darker: Color
    dark: Color
    light: Color
    lighter: Color
    lightest: Color


COLOR_PALETTE = ColorPalette(
    Color("#272744"),
    Color("#494d7e"),
    Color("#8b6d9c"),
    Color("#c69fa5"),
    Color("#f2d3ab"),
    Color("#fbf5ef"),
)
