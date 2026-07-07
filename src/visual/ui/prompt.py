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
        message: str,
        is_alert: bool,
    ) -> None:
        super().__init__(context)
        self.text = context.font.render(message, False, Color("white"))
        ok_text = context.font.render("Ok", False, Color("white"))
        ok_button = Button(
            context, ok_text, Vector2(50, 30), Color("green"), lambda: None
        )
        ok_button.local_position = Vector2(50, 50)
        self.add_child(ok_button)

    def _on_draw(self) -> None:
        draw.rect(
            self.context.screen,
            Color("grey"),
            Rect(self.world_position, Vector2(300, 200)),
        )
        self.context.screen.blit(self.text, self.world_position)
