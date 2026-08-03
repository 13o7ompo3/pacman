"""A module that defines a Prompt."""

from typing import Callable

import pygame
from pygame import (
    K_RETURN,
    Surface,
    Vector2,
)
from pygame.event import Event

from src.visual import Context, Node
from src.visual.draw import Draw
from src.visual.ui.button import Button


class Prompt(Node):
    """A class that represents a prompt.

    Attributes:
        title (Surface): The title of the prompt.
        message (Surface): The message of the prompt.
        size (Vector2): The size of the prompt.
        content (Surface): The content of the prompt.

    """

    def __init__(
        self,
        context: Context,
        title: str,
        message: str,
        on_accept: Callable,
    ) -> None:
        """Initialize a Prompt instance."""
        super().__init__(context)
        self.title = self.context.assets.font("ui").render(
            title, False, context.colors.lightest
        )
        self.message = self.context.assets.font("ui").render(
            message, False, context.colors.lightest
        )

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

        Draw.rect(
            self.content,
            (0, 0),
            self.size,
            fill_color=context.colors.darker,
            border_color=context.colors.lightest,
            border_radius=7,
            border_width=1,
        )
        Draw.rect(
            self.content,
            (int(padding.x), int(self.title.get_size()[1] + padding.y * 2)),
            (
                int(self.size.x - 2 * padding.x),
                2,
            ),
            fill_color=context.colors.lightest,
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
                context.colors.light,
                on_accept_fn,
                {K_RETURN},
                shadow_color=context.colors.dark,
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
        """Draw the prompt on the screen."""
        self.context.screen.blit(self.content, self.world_position)

    def _on_input(self, event: Event) -> Event | None:
        """Stop input events from propagating to other nodes.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event if it was not handled, otherwise None.

        """
        return
