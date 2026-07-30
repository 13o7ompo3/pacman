from pygame import K_t, KEYUP
from pygame.event import Event
from src.visual import Node, Context
from src.visual.palette import ColorPalette
from src.visual.utils.asset_manager import AssetManager


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
            self.current_theme_index = (self.current_theme_index + 1) % len(
                self.themes
            )
            theme = self.themes[self.current_theme_index]
            self._copy_color(self.context.colors.darkest, theme.darkest)
            self._copy_color(self.context.colors.darker, theme.darker)
            self._copy_color(self.context.colors.dark, theme.dark)
            self._copy_color(self.context.colors.light, theme.light)
            self._copy_color(self.context.colors.lighter, theme.lighter)
            self._copy_color(self.context.colors.lightest, theme.lightest)
            self.redraw()

    def _copy_color(self, color1, color2) -> None:
        color1.r = color2.r
        color1.g = color2.g
        color1.b = color2.b
        color1.a = color2.a
