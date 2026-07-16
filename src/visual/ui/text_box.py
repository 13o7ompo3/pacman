from pygame import Color, Rect, Surface, Vector2, draw
from src.visual import Node, Context
from pygame.event import Event
import pygame


class TextBox(Node):
    def __init__(self, context: Context, size: Vector2) -> None:
        super().__init__(context)
        self.size = size
        self.content = ""
        self.text: Surface | None = None

    def _on_input(self, event: Event) -> Event | None:
        if event.type == pygame.KEYDOWN:
            self.text += event.unicode
        return event

    def _on_draw(self) -> None:
        draw.rect(
            self.context.screen,
            Color("white"),
            Rect(self.world_position, self.size),
            border_radius=2,
        )
        draw.rect(
            self.context.screen,
            Color("gray"),
            Rect(self.world_position, self.size),
            width=2,
            border_radius=2,
        )
