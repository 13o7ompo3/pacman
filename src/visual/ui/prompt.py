from src.visual import Context, Node
from pygame import (
    BLEND_RGBA_MULT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    Color,
    Rect,
    Surface,
    Vector2,
)
from pygame.font import Font
from pygame.event import Event
from pygame import draw
from typing import Any, Callable
from src.visual.ui.button import Button


class Prompt(Node):
    def __init__(
        self,
        context: Context,
        title: str,
        message: str,
        is_alert: bool,
    ) -> None:
        super().__init__(context)
        self.title = context.font.render(title, False, Color("white"))
        self.message = context.font.render(message, False, Color("white"))

        self.size = Vector2(
            max(self.title.get_size()[0], self.message.get_size()[0]),
            self.title.get_size()[1] + self.message.get_size()[1],
        )

        self.local_position = (
            Vector2(self.context.width, self.context.height) / 2
            - self.size / 2
        )

        ok_text = context.font.render("Ok", False, Color("white"))
        ok_button = Button(
            context, ok_text, Vector2(50, 30), Color("green"), lambda: None
        )
        self.add_child(ok_button)

    def _on_draw(self) -> None:
        draw.rect(
            self.context.screen,
            Color("blue"),
            Rect(self.world_position, self.size),
            border_radius=7,
        )
        draw.rect(
            self.context.screen,
            Color("white"),
            Rect(self.world_position, self.size),
            width=1,
            border_radius=7,
        )
        draw.line(
            self.context.screen,
            Color("white"),
            (0, 0),
            self.world_position + self.size,
        )
        self.context.screen.blit(self.title, self.world_position)
        self.context.screen.blit(
            self.message,
            self.world_position + Vector2(0, self.title.get_size()[1]),
        )
