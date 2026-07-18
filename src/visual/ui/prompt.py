from src.visual import Context, Node
from pygame import (
    K_RETURN,
    Color,
    Rect,
    Surface,
    Vector2,
)
import pygame
from pygame.font import Font
from pygame.event import Event
from pygame import draw, Surface
from typing import Any, Callable
from src.visual.ui.button import Button


class Prompt(Node):
    def __init__(
        self,
        context: Context,
        title: str,
        message: str,
        on_accept: Callable,
    ) -> None:
        super().__init__(context)
        self.title = context.font.render(title, False, Color("white"))
        self.message = context.font.render(message, False, Color("white"))

        padding = Vector2(10, 10)
        button_size = Vector2(50, 30)

        self.size = Vector2(
            max(self.title.get_size()[0], self.message.get_size()[0]),
            self.title.get_size()[1] + self.message.get_size()[1],
        ) + Vector2(padding.x * 2, padding.y * 5 + button_size.y)

        self.local_position = (
            Vector2(self.context.width, self.context.height) / 2
            - self.size / 2
        )
        self.content = Surface(self.size, flags=pygame.SRCALPHA)

        draw.rect(
            self.content,
            Color("blue"),
            Rect((0, 0), self.size),
            border_radius=7,
        )
        draw.rect(
            self.content,
            Color("white"),
            Rect((0, 0), self.size),
            width=1,
            border_radius=7,
        )
        draw.line(
            self.content,
            Color("white"),
            (padding.x, self.title.get_size()[1] + padding.y * 2),
            (
                self.size.x - padding.x,
                self.title.get_size()[1] + padding.y * 2,
            ),
        )
        self.content.blit(
            self.title,
            (
                self.size.x / 2 - self.title.get_size()[0] / 2,
                padding.y,
            ),
        )
        self.content.blit(
            self.message,
            (padding.x, padding.y * 3 + self.title.get_size()[1]),
        )

        def on_accept_fn(_):
            on_accept(self)
            self.free_from_scene()

        buttons = [
            Button(
                context,
                "Ok",
                button_size,
                Color("green"),
                on_accept_fn,
                {K_RETURN},
            ),
        ]

        for i, button in enumerate(buttons):
            button.local_position = self.world_position + Vector2(
                self.size.x * i / len(buttons)
                + self.size.x * 0.5 / len(buttons)
                - button_size.x / 2,
                padding.y * 4
                + self.title.get_size()[1]
                + self.message.get_size()[1],
            )
            self.add_child(button)

    def _on_draw(self) -> None:
        self.context.screen.blit(self.content, self.world_position)

    def _on_input(self, event: Event) -> Event | None:
        return
