from pygame import K_t, KEYUP, Surface
from pygame.event import Event
from src.visual import Node, Context
from src.visual.utils.image import Image
from src.visual.palette import ColorPalette
from src.visual.utils.asset_manager import AssetManager
from copy import deepcopy


class RootScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        self.current_theme_index = 0
        self.themes = None

    def load_themes(self):
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

    def _on_input(self, event: Event) -> Event | None:
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
        color1.r = color2.r
        color1.g = color2.g
        color1.b = color2.b
        color1.a = color2.a
