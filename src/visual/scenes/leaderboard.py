"""A module that defines the LeaderBoardScene class."""

from src.visual import Node, Context
from src.visual.ui.label import Label
from src.visual.ui.panel import Panel
from pygame import Vector2, MOUSEBUTTONDOWN
from pygame.event import Event


class LeaderBoardScene(Node):
    """A class that represents the leaderboard scene.

    Attributes:
        entries (list[Label]): A list of Label objects representing scores.

    """

    def __init__(self, context: Context) -> None:
        """Initialize a LeaderBoardScene instance."""
        super().__init__(context)
        width, height = context.width, context.height
        panel = Panel(
            context,
            Vector2(300, 350),
            context.colors.darker,
            border_color=context.colors.darkest,
            on_outside_press=lambda x: self.free_from_scene(),
        )
        panel.local_position = Vector2(
            width / 2 - panel.size.x / 2, height / 7
        )
        self.add_child(panel)

        title_text = Label(
            context,
            Vector2(300, 200),
            [("LeaderBoard", context.colors.lightest)],
            2,
        )
        title_text.local_position = (
            Vector2(width / 2, height / 5) - title_text.size / 2
        )
        self.add_child(title_text)

        self.entries = []
        for i, user in enumerate(context.user_manager.get_leaderboard()[:10]):
            entry = Label(
                context,
                Vector2(panel.size.x, panel.size.y / 12),
                [
                    (f"{user.username}:    ", context.colors.light),
                    (str(user.highscore), context.colors.lighter),
                ],
            )
            entry.local_position = Vector2(0, (panel.size.y * (i + 2)) / 13)
            self.entries.append(entry)
            panel.add_child(entry)

    def _on_input(self, event: Event) -> Event | None:
        """Handle input events for the leaderboard scene.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event if it was not handled, otherwise None.

        """
        if event.type == MOUSEBUTTONDOWN:
            self.context.root_scene.remove_child(self)
