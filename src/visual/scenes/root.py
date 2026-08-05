"""Root scene for the game."""

from pygame import K_t, KEYUP
from pygame.event import Event
from src.visual import Node, Context
from src.visual.utils.image import Image
from src.visual.palette import ColorPalette
from copy import deepcopy
from src.visual.utils.parallax import Parallax


class RootScene(Node):
    """A class that represents the root scene of the game.

    Attributes:
        current_theme_index (int): The index of the current color theme.
        themes (list[ColorPalette]): A list of color themes.

    """

    def __init__(self, context: Context) -> None:
        """Initialize a RootScene instance."""
        super().__init__(context)
        self.current_theme_index = 0
        self.themes = None

    def load_themes(self):
        """Load color themes from assets."""
        self.themes = [
            ColorPalette.load_from_surface(
                self.context.assets.image("cryptic-ocean_palette")
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("robots-are-cool_palette")
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("molten_palette")
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("enbydiade6_palette")
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("vintage-voltage_palette")
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("bluberry-6_palette")
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("grape-soda-arcade_palette")
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("fistat6_palette")
            ),
        ]
        parallax = Parallax(
            self.context,
            [
                (self.context.assets.image("background_layer1"), 0.2),
                (self.context.assets.image("background_layer2"), 0.4),
                (self.context.assets.image("background_layer3"), 0.6),
                (self.context.assets.image("background_layer4"), 0.8),
            ],
            40,
        )
        self.add_child(parallax)
        self.children = self.children[::-1]

    def _on_input(self, event: Event) -> Event | None:
        """Handle input events for the root scene.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event if it was not handled, otherwise None.

        """
        if event.type == KEYUP and event.key == K_t and self.themes:
            old_theme = deepcopy(self.context.colors)
            self.current_theme_index = (self.current_theme_index + 1) % len(
                self.themes
            )
            new_theme = self.themes[self.current_theme_index]
            self._copy_color(self.context.colors.darkest, new_theme.darkest)
            self._copy_color(self.context.colors.darker, new_theme.darker)
            self._copy_color(self.context.colors.dark, new_theme.dark)
            self._copy_color(self.context.colors.light, new_theme.light)
            self._copy_color(self.context.colors.lighter, new_theme.lighter)
            self._copy_color(self.context.colors.lightest, new_theme.lightest)

            for image in self.context.assets.images:
                surface = self.context.assets.image(image)
                Image.switch_palette(surface, old_theme, new_theme)

            self.redraw()

    def _copy_color(self, color1, color2) -> None:
        """Copy the RGBA values from one color to another.

        Args:
            color1: The color to copy to.
            color2: The color to copy from.

        """
        color1.r = color2.r
        color1.g = color2.g
        color1.b = color2.b
        color1.a = color2.a
