"""A button UI element for the game."""

from typing import Any, Callable

import pygame
from pygame import (
    BLEND_RGBA_MULT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    Color,
    Rect,
    Surface,
    Vector2,
)
from pygame.event import Event

from src.visual import Context, Node
from src.visual.draw import Draw


class Button(Node):
    """A class that represents a button.

    Attributes:
        context (Context): The context of the button.
        fg_color (Color): The foreground color of the button.
        bg_color (Color): The background color of the button.
        border_color (Color): The border color of the button.
        padding (int): The padding around the content of the button.
        content (Surface): The content of the button.
        original_content (Surface): The original content of the button.
        size (Vector2): The size of the button.
        thickness (int): The thickness of the button's border.
        border_radius (int): The radius of the button's border corners.
        bg_rect (Rect): The rectangle representing the button's background.
        fg_rect (Rect): The rectangle representing the button's foreground.
        pressed_rect (Rect): The rectangle representing if the button pressed.
        content_position (Vector2): The position of the content on the button.
        pressed_content_position (Vector2): The position when pressed.
        is_hovered (bool): A flag indicating if the button is hovered.
        is_pressed (bool): A flag indicating if the button is pressed.
        is_shortcut_down (bool): A flag indicating if a shortcut key pressed.
        callback (Callable): The callback function to be called when pressed.

    """

    def __init__(
        self,
        context: Context,
        content: str | Surface | list[Surface | str],
        size: Vector2,
        color: Color,
        callback: Callable,
        shortcuts: set[int] = set(),
        thickness: int = 5,
        border_radius: int = 4,
        shadow_color: Color | None = None,
        highlight_color: Color | None = None,
        padding: int = 3,
    ) -> None:
        """Initialize a Button instance."""
        self.context = context
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

        self.padding = padding
        self.content = self._prepare_content(content)
        self.original_content = self.content.copy()
        self.content.fill(self.bg_color, special_flags=BLEND_RGBA_MULT)
        size = Vector2(
            max(size.x, self.content.get_size()[0]),
            max(size.y, self.content.get_size()[1]),
        )
        self.size = size

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

    def _prepare_content(
        self,
        content: str | Surface | list[Surface | str],
    ) -> Surface:
        """Prepare the content for the button.

        Args:
            content (str | Surface | list[Surface | str]): The content.

        Returns:
            Surface: The prepared content as a Pygame Surface.

        """
        if isinstance(content, str):
            content = (
                self.context.assets.font("ui")
                .render(
                    content,
                    False,
                    Color("white"),
                )
                .convert_alpha()
            )
        elif isinstance(content, list):
            size = Vector2()
            for i in range(len(content)):
                if isinstance(content[i], str):
                    content[i] = (
                        self.context.assets.font("ui")
                        .render(
                            content[i],
                            False,
                            Color("white"),
                        )
                        .convert_alpha()
                    )
                elif isinstance(content[i], Surface):
                    content[i] = content[i]
                w, h = content[i].get_size()
                size.x += w
                if h > size.y:
                    size.y = h

            size += Vector2(
                self.padding * (len(content) + 1), self.padding * 2
            )
            surface = Surface(size, flags=pygame.SRCALPHA)
            x = self.padding
            for i in range(len(content)):
                w, h = content[i].get_size()
                surface.blit(content[i], (x, size.y / 2 - h / 2))
                x += w + self.padding
            content = surface
        elif isinstance(content, Surface):
            content = content.convert_alpha()

        return content

    def __setattr__(self, name: str, value: Any, /) -> None:
        """Set an attribute and update the button rectangle position if needed.

        Args:
            name (str): The name of the attribute.
            value (Any): The value to set for the attribute.

        """
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
        """Handle input events for the button.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event if it was not handled, otherwise None.

        """
        if hasattr(event, "pos"):
            x, y = event.pos
            self.is_hovered = self.bg_rect.collidepoint(x, y)

        if self.is_hovered:
            if event.type == MOUSEBUTTONDOWN:
                self.is_pressed = True
            elif event.type == MOUSEBUTTONUP and self.is_pressed:
                self.is_pressed = False
                self.callback(self)
        elif not self.is_shortcut_down:
            self.is_pressed = False

        if event.type == pygame.KEYDOWN and event.key in self.shortcuts:
            self.is_pressed = True
            self.is_shortcut_down = True
        elif event.type == pygame.KEYUP and event.key in self.shortcuts:
            self.is_pressed = False
            self.is_shortcut_down = False
            self.callback(self)

        return event

    def _on_draw(self) -> None:
        """Draw the button on the screen."""
        if self.is_pressed:
            Draw.rect(
                self.context.screen,
                self.pressed_rect.topleft,
                self.pressed_rect.size,
                fill_color=self.fg_color,
                border_color=Color("white"),
                border_radius=self.border_radius,
                border_width=1,
            )
            self.context.screen.blit(
                self.content, self.pressed_content_position
            )
        else:
            Draw.rect(
                self.context.screen,
                self.bg_rect.topleft,
                self.bg_rect.size,
                fill_color=self.bg_color,
                border_radius=self.border_radius,
            )
            Draw.rect(
                self.context.screen,
                self.fg_rect.topleft,
                self.fg_rect.size,
                fill_color=self.fg_color,
                border_radius=self.border_radius,
            )
            Draw.rect(
                self.context.screen,
                self.bg_rect.topleft,
                self.bg_rect.size,
                border_color=Color("white")
                if self.is_hovered
                else self.border_color,
                border_width=1,
                border_radius=self.border_radius,
            )
            self.context.screen.blit(self.content, self.content_position)

    def _on_redraw(self) -> None:
        """Redraw the button."""
        self.content = self.original_content.copy()
        self.content.fill(self.bg_color, special_flags=BLEND_RGBA_MULT)
