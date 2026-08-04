"""Define a panel UI element."""

from src.visual import Node, Context
from src.visual.draw import Draw
from pygame import (
    Color,
    Surface,
    Vector2,
    Rect,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
)
from pygame.event import Event
from typing import Any, Callable
import pygame


class Panel(Node):
    """A class that represents a panel.

    Attributes:
        size (Vector2): The size of the panel.
        rect (Rect): The rectangle representing the panel's position and size.
        on_inside_press (Callable): A callback when pressed inside.
        on_outside_press (Callable): A callback when pressed outside.
        is_pressed (bool): A flag indicating when mouse button down.

    """

    def __init__(
        self,
        context: Context,
        size: Vector2,
        color: Color,
        on_inside_press: Callable = lambda _: None,
        on_outside_press: Callable = lambda _: None,
        border_color: Color | None = None,
        border_width: int = 5,
        outer_border_color: Color | None = None,
        border_radius: int = 8,
    ) -> None:
        """Initialize a Panel instance."""
        self.size = size
        self.rect = Rect((0, 0), self.size)
        self.on_inside_press = on_inside_press
        self.on_outside_press = on_outside_press
        self.is_pressed = False

        outer_border_color = (
            outer_border_color
            if outer_border_color
            else context.colors.lightest
        )

        self.surface = Surface(self.size, flags=pygame.SRCALPHA)
        if border_color is None:
            border_color = color.lerp("darkblue", 0.3)

        Draw.rect(
            self.surface,
            self.rect.topleft,
            self.rect.size,
            fill_color=color,
            border_color=border_color,
            border_width=border_width,
            border_radius=border_radius,
        )
        Draw.rect(
            self.surface,
            self.rect.topleft,
            self.rect.size,
            border_width=1,
            border_color=outer_border_color,
            border_radius=border_radius,
        )
        super().__init__(context)

    def __setattr__(self, name: str, value: Any) -> Any:
        """Set an attribute and update the panel rectangle position if needed.

        Args:
            name (str): The name of the attribute.
            value (Any): The value to set for the attribute.

        Returns:
            Any: The result of the attribute setting operation.

        """
        ret = super().__setattr__(name, value)
        if name == "local_position":
            x, y = self.world_position
            self.rect.topleft = (int(x), int(y))
        return ret

    def _on_draw(self) -> None:
        """Draw the panel on the screen."""
        self.context.screen.blit(self.surface, self.world_position)

    def _on_input(self, event: Event) -> Event | None:
        """Handle input events for the panel.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event if it was not handled, otherwise None.

        """
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
