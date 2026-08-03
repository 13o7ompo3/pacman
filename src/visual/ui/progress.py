"""Defines a progress bar UI element."""

from enum import Enum
from typing import Callable

from pygame import Color, Rect, Vector2, draw
from src.visual import Node, Context
from src.visual.draw import Draw


class ProgressBarOrientation(Enum):
    """An enumeration for progress bar orientation.

    Attributes:
        VERTICAL (str): Represents a vertical progress bar.
        HORIZONTAL (str): Represents a horizontal progress bar.
    """

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class ProgressBar(Node):
    """A class that represents a progress bar.

    Attributes:
        size (Vector2): The size of the progress bar.
        orientation (ProgressBarOrientation): The orientation of the progress.
        progress_color (Color): The color of the progress indicator.
        total (float): The total value for the progress bar.
        reversed (bool): Whether the progress bar is reversed.
        border_color (Color | None): The color of the border.
        border_width (int): The width of the border.
        border_radius (int): The radius of the border corners.
        on_finish (Callable): A callback function when progress reaches total.

    """

    def __init__(
        self,
        context: Context,
        size: Vector2,
        orientation: ProgressBarOrientation,
        progress_color: Color,
        total: float = 1.0,
        reversed: bool = False,
        border_color: Color | None = None,
        border_width: int = 2,
        border_radius: int = 7,
        on_finish: Callable = lambda _: None,
    ) -> None:
        """Initialize a ProgressBar instance."""
        super().__init__(context)

        self.size = size
        self.orientation = orientation
        self.progress_color = progress_color
        self.total = total
        self.reversed = reversed
        self.border_color = (
            border_color if border_color else context.colors.lightest
        )
        self.border_width = border_width
        self.border_radius = border_radius
        self.on_finish = on_finish
        self._progress = 0
        self._animated_progress = 0

    @property
    def progress(self) -> float:
        """Get the current progress value.

        Returns:
            float: The current progress value.

        """
        return self._progress

    @progress.setter
    def progress(self, value: float):
        """Set the current progress value.

        Args:
            value (float): The new progress value.

        """
        if self.reversed:
            self._progress = self.total - value
        else:
            self._progress = value

        if self._progress > self.total:
            self._progress = self.total
        if self._progress < 0:
            self._progress = 0

        if self._progress == self.total:
            self.on_finish(self)

    def _on_draw(self) -> None:
        """Draw the progress bar on the screen."""
        inflate = Vector2()
        if self.orientation is ProgressBarOrientation.VERTICAL:
            progress = Vector2(
                self.size.x,
                self.size.y * self._progress / self.total if self.total else 0,
            )
            if progress.y < (self.border_radius * 2 + 2):
                inflate.x = (self.border_radius * 2 + 2) - progress.y
        else:
            progress = Vector2(
                self.size.x * self._progress / self.total if self.total else 0,
                self.size.y,
            )
            if progress.x < (self.border_radius * 2 + 2):
                inflate.y = (self.border_radius * 2 + 2) - progress.x
        progress_rect = Rect(
            self.world_position,
            progress,
        ).inflate(-inflate.x, -inflate.y)

        Draw.rect(
            self.context.screen,
            progress_rect.topleft,
            progress_rect.size,
            fill_color=self.progress_color,
            border_radius=self.border_radius,
        )
        Draw.rect(
            self.context.screen,
            self.world_position,
            self.size,
            border_color=self.border_color,
            border_width=self.border_width,
            border_radius=self.border_radius,
        )
