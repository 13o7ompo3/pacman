"""Root scene for the game."""

from typing import Iterator
from pygame import K_t, KEYUP, Vector2
from pygame.event import Event
from src.visual import Node, Context
from src.visual.ui.progress import ProgressBar, ProgressBarOrientation
from src.visual.ui.prompt import Prompt
from src.visual.utils.image import Image
from src.visual.palette import ColorPalette
from copy import deepcopy
from src.visual.utils.parallax import Parallax
from random import shuffle
import logging


logger = logging.getLogger(__name__)


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
        self.loading_iter: Iterator | None = None

    def finish_loading(self):
        """Load color themes from assets."""
        self.themes = [
            ColorPalette.load_from_surface(
                self.context.assets.image("6353yh4-redux-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("6-violets-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("ash-persimmon-6-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("black-and-white-6-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("blackhole6-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("bluberry-6-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("blue-screen-of-palette-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("cave6-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("cryptic-ocean-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("depths-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("enbydiade6-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("fistat6-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("grape-soda-arcade-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("ice-cream-land-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("icywitch-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("inkpink-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("lavendertown-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("midnight-epipelagic-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("monometalic-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("noelles-room-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("robots-are-cool-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("roserust-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("sandy-06-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("sepia6-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("spooky6-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("teaviie-1x"),
            ),
            ColorPalette.load_from_surface(
                self.context.assets.image("vintage-voltage-1x"),
            ),
        ]
        shuffle(self.themes)
        self.parallax_background = Parallax(
            self.context,
            [
                (self.context.assets.image("background_layer1"), 0.2),
                (self.context.assets.image("background_layer2"), 0.4),
                (self.context.assets.image("background_layer3"), 0.6),
                (self.context.assets.image("background_layer4"), 0.8),
            ],
            40,
        )
        self.children.insert(0, self.parallax_background)

    def clear_children(self) -> None:
        """Clear all children of the root node except the background."""
        if hasattr(self, "parallax_background"):
            del self.children[1:]
        else:
            super().clear_children()

    def _on_input(self, event: Event) -> Event | None:
        """Handle input events for the root scene.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event if it was not handled, otherwise None.

        """
        if event.type == KEYUP and event.key == K_t:
            self.change_theme()

    def change_theme(self) -> None:
        self.loading_iter = self.cycle_theme()

    def cycle_theme(self) -> Iterator:
        loading_alert = Prompt(
            self.context,
            "Loading new theme..",
            "",
            lambda _: None,
        )
        loading_bar = ProgressBar(
            self.context,
            Vector2(loading_alert.content.get_size()[0] - 30, 20),
            ProgressBarOrientation.HORIZONTAL,
            self.context.colors.light,
            total=len(self.context.assets.images),
        )
        loading_alert.add_child(loading_bar)
        loading_bar.local_position = (
            Vector2(loading_alert.content.get_size()) / 2
            - loading_bar.size / 2
        )

        self.context.root_scene.add_child(loading_alert)

        for child_node in self.context.root_scene.children:
            child_node.paused = True

        if self.themes:
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
                loading_bar.progress += 1
                yield

        for child_node in self.context.root_scene.children:
            child_node.paused = False

        loading_alert.free_from_scene()
        loading_bar.free_from_scene()
        logger.info("color palette changed successfully")
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

    def _on_update(self, delta: float) -> None:
        if self.loading_iter is not None:
            try:
                next(self.loading_iter)
            except StopIteration:
                self.loading_iter = None
