from src.visual import Node, Context
from src.visual.ui.label import Label
from pygame import Color, Vector2, Rect, draw
from pygame.event import Event


class Panel(Node):
    def __init__(
        self,
        context: Context,
        size: Vector2,
        color: Color,
        border_color: Color,
        border_width: int,
        border_radius: int,
    ) -> None:
        super().__init__(context)
        self.size = size
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius

    def _on_draw(self) -> None:
        draw.rect(
            self.context.screen,
            self.color,
            Rect(self.world_position, self.size),
            self.border_width,
            self.border_radius,
        )
