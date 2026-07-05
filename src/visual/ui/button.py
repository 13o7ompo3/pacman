from src.visual import Node
from pygame import KEYDOWN, MOUSEBUTTONUP, Color, Rect, Surface, Vector2
from pygame.event import Event
from pygame import draw
from typing import Any, Callable


class Button(Node):
    def __init__(
        self, callback: Callable, size: Vector2 = Vector2(35, 20)
    ) -> None:
        super().__init__()
        self.size = size
        self.callback = callback
        self.rect = Rect(self.world_position, self.size)

    def _on_update(self, delta: float) -> None:
        self.rect = Rect(self.world_position, self.size)

    def _on_input(self, event: Event) -> None:
        if event.type == MOUSEBUTTONUP:
            x, y = event.pos
            if self.rect.collidepoint(x, y):
                self.callback()

    def _on_draw(self, screen: Surface) -> None:
        draw.rect(screen, Color("blue"), self.rect)
