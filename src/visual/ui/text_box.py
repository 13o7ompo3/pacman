"""Defines a text box UI element for user input."""

from pygame import Vector2
from src.visual.draw import Draw
from src.visual import Node, Context
from pygame.event import Event
import pygame
from typing import Callable


class TextBox(Node):
    """A class that represents a text box.

    Attributes:
        content (str): The current text content of the text box.
        length (int): The maximum length of the text box.
        on_submit (Callable): A callback function when the user submits.
        is_password (bool): A flag indicating if the text box is for password.
        size (Vector2): The size of the text box.
        text_pos (Vector2): The position of the text within the text box.

    """

    def __init__(
        self,
        context: Context,
        length: int,
        on_submit: Callable,
        is_password: bool = False,
    ) -> None:
        """Initialize a TextBox instance."""
        super().__init__(context)
        self.is_password = is_password
        self.content = ""
        self.length = length
        self.on_submit = on_submit
        box_size = Vector2(
            self.context.assets.font("ui").size(" ")[0] * length,
            self.context.assets.font("ui").size(" ")[1],
        )
        self.size = Vector2(
            box_size.y * 0.4 + box_size.x,
            box_size.y * 1.4,
        )
        self.text_pos = Vector2(
            box_size.y * 0.2,
            self.size.y / 2 - box_size.y / 2,
        )

    @property
    def content(self) -> str:
        """Get the current content of the text box.

        Returns:
            str: The current text content of the text box.

        """
        return self._content

    @content.setter
    def content(self, val: str):
        """Set the current content of the text box.

        Args:
            val (str): The new text content of the text box.

        """
        self._content = val
        if self.is_password:
            content = "*" * len(self.content)
        else:
            content = self.content
        self.text = self.context.assets.font("ui").render(
            content, False, self.context.colors.dark
        )

    def _on_input(self, event: Event) -> Event | None:
        """Handle input events for the text box.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event if it was not handled, otherwise None.

        """
        if self.hidden:
            return event

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                self.on_submit(self)
            elif event.key == pygame.K_BACKSPACE:
                self.content = self.content[:-1]
            elif len(self.content) < self.length:
                self.content += event.unicode

    def _on_draw(self) -> None:
        """Draw the text box on the screen."""
        Draw.rect(
            self.context.screen,
            self.world_position,
            self.size,
            fill_color=self.context.colors.lightest,
            border_color=self.context.colors.lighter,
            border_radius=2,
            border_width=2,
        )
        if self.text is not None:
            self.context.screen.blit(
                self.text, self.world_position + self.text_pos
            )
