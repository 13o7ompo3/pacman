from src.visual import Node, Context
from src.visual.ui.label import Label
from pygame import (
    Color,
    Surface,
    Vector2,
    Rect,
    draw,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
)
from pygame.event import Event
from typing import Any, Callable


class Panel(Node):
    def __init__(
        self,
        context: Context,
        size: Vector2,
        color: Color,
        on_inside_press: Callable = lambda: None,
        on_outside_press: Callable = lambda: None,
        border_color: Color | None = None,
        border_width: int = 5,
        outer_border_color: Color = Color("white"),
        border_radius: int = 8,
    ) -> None:
        self.size = size
        self.rect = Rect((0, 0), self.size)
        self.on_inside_press = on_inside_press
        self.on_outside_press = on_outside_press
        self.is_pressed = False

        self.surface = Surface(self.size)
        if border_color is None:
            border_color = color.lerp("darkblue", 0.3)

        draw.rect(
            self.surface,
            color,
            self.rect,
            0,
            border_radius,
        )
        draw.rect(
            self.surface,
            border_color,
            self.rect,
            border_width,
            border_radius,
        )
        draw.rect(
            self.surface,
            outer_border_color,
            self.rect,
            1,
            border_radius,
        )
        super().__init__(context)

    def __setattr__(self, name: str, value: Any, /) -> None:
        ret = super().__setattr__(name, value)
        if name == "local_position":
            x, y = self.world_position
            self.rect.topleft = (int(x), int(y))
        return ret

    def _on_draw(self) -> None:
        self.context.screen.blit(self.surface, self.world_position)

    def _on_input(self, event: Event) -> Event | None:
        if hasattr(event, "pos"):
            x, y = event.pos
            is_hovering = self.rect.collidepoint(x, y)
            if is_hovering:
                if event.type == MOUSEBUTTONDOWN:
                    self.is_pressed = True
                elif event.type == MOUSEBUTTONUP and self.is_pressed:
                    self.is_pressed = False
                    self.on_inside_press(self)
            elif event.type == MOUSEBUTTONUP:
                self.on_outside_press(self)
