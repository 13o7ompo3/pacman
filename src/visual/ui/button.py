from src.visual import Context, Node
from pygame import (
    BLEND_RGBA_MULT,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    Color,
    Rect,
    Surface,
    Vector2,
)
from pygame.event import Event
from pygame import draw
from typing import Any, Callable
import pygame


class Button(Node):
    def __init__(
        self,
        context: Context,
        content: Surface | str,
        size: Vector2,
        color: Color,
        callback: Callable,
        shortcuts: set[int] = set(),
        thickness: int = 5,
        border_radius: int = 8,
        shadow_color: Color | None = None,
        highlight_color: Color | None = None,
    ) -> None:
        self.size = size
        self.fg_color = color
        self.bg_color = (
            shadow_color
            if shadow_color
            else color.lerp(Color("darkblue"), 0.4)
        )
        self.border_color = (
            highlight_color
            if highlight_color
            else color.lerp(Color("lightyellow"), 0.4)
        )

        if isinstance(content, str):
            self.content = context.font.render(
                content,
                False,
                self.bg_color,
            ).convert_alpha()
        else:
            self.content = content.convert_alpha()
            self.content.fill(self.bg_color, special_flags=BLEND_RGBA_MULT)

        self.thickness = thickness
        self.border_radius = border_radius

        self.bg_rect = Rect(Vector2(0), size)
        self.bg_rect.height += thickness
        self.fg_rect = Rect(Vector2(0), size)

        self.pressed_rect = Rect(Vector2(0), size)
        self.pressed_rect.y += thickness

        self.content_position = Vector2()
        self.pressed_content_position = Vector2()

        self.is_hovered = False
        self.is_pressed = False
        self.is_shortcut_down = False

        self.callback = callback
        self.shortcuts = shortcuts

        super().__init__(context)

    def __setattr__(self, name: str, value: Any, /) -> None:
        ret = super().__setattr__(name, value)
        if name == "local_position":
            x, y = self.world_position
            self.bg_rect.topleft = (int(x), int(y))
            self.fg_rect.topleft = (int(x), int(y))
            self.pressed_rect.topleft = (int(x), int(y) + self.thickness)
            self.content_position = (
                Vector2(self.fg_rect.center)
                - Vector2(self.content.get_size()) / 2
                + Vector2(1)
            )
            self.pressed_content_position = self.content_position.copy()
            self.pressed_content_position.y += self.thickness
        return ret

    def _on_input(self, event: Event) -> Event | None:
        if hasattr(event, "pos"):
            x, y = event.pos
            self.is_hovered = self.bg_rect.collidepoint(x, y)

        if self.is_hovered:
            if event.type == MOUSEBUTTONDOWN:
                self.is_pressed = True
            elif event.type == MOUSEBUTTONUP and self.is_pressed:
                self.is_pressed = False
                self.callback()
        elif not self.is_shortcut_down:
            self.is_pressed = False

        if event.type == pygame.KEYDOWN and event.key in self.shortcuts:
            self.is_pressed = True
            self.is_shortcut_down = True
        elif event.type == pygame.KEYUP and event.key in self.shortcuts:
            self.is_pressed = False
            self.is_shortcut_down = False
            self.callback()

        return event

    def _on_draw(self) -> None:
        if self.is_pressed:
            draw.rect(
                self.context.screen,
                self.fg_color,
                self.pressed_rect,
                border_radius=self.border_radius,
            )
            draw.rect(
                self.context.screen,
                Color("white"),
                self.pressed_rect,
                1,
                self.border_radius,
            )
            self.context.screen.blit(
                self.content, self.pressed_content_position
            )
        else:
            draw.rect(
                self.context.screen,
                self.bg_color,
                self.bg_rect,
                border_radius=self.border_radius,
            )
            draw.rect(
                self.context.screen,
                self.fg_color,
                self.fg_rect,
                border_radius=self.border_radius,
            )
            draw.rect(
                self.context.screen,
                Color("white") if self.is_hovered else self.border_color,
                self.bg_rect,
                1,
                self.border_radius,
            )
            self.context.screen.blit(self.content, self.content_position)
