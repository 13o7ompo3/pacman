from pygame import Color, Rect, Surface, Vector2, draw
from src.visual import Node, Context
from pygame.event import Event
import pygame
from typing import Callable


class TextBox(Node):
    def __init__(
        self,
        context: Context,
        length: int,
        on_submit: Callable,
        is_password: bool = False,
    ) -> None:
        super().__init__(context)
        self.content = ""
        self.length = length
        self.on_submit = on_submit
        box_size = Vector2(
            context.font.size(" ")[0] * length, context.font.size(" ")[1]
        )
        self.size = Vector2(
            box_size.y * 0.4 + box_size.x,
            box_size.y * 1.4,
        )
        self.text_pos = Vector2(
            box_size.y * 0.2,
            self.size.y / 2 - box_size.y / 2,
        )
        self.text = self.context.font.render(self.content, False, Color("red"))
        self.is_password = is_password

    def _on_input(self, event: Event) -> Event | None:
        if self.hidden:
            return event

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.on_submit(self)
            elif event.key == pygame.K_BACKSPACE:
                self.content = self.content[:-1]
            elif len(self.content) < self.length:
                self.content += event.unicode
            if self.is_password:
                content = "*" * len(self.content)
            else:
                content = self.content
            self.text = self.context.font.render(content, False, Color("red"))
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
        if self.text is not None:
            self.context.screen.blit(
                self.text, self.world_position + self.text_pos
            )
