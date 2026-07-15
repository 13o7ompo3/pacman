from enum import Enum

from pygame import Color, Rect, Vector2, draw
from src.visual import Node, Context


class ProgressBarOrientation(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class ProgressBar(Node):
    def __init__(
        self,
        context: Context,
        size: Vector2,
        orientation: ProgressBarOrientation,
        progress_color: Color,
        total: float = 1.0,
        reversed: bool = False,
        border_color: Color = Color("white"),
        border_width: int = 2,
        border_radius: int = 7,
    ) -> None:
        super().__init__(context)

        self.size = size
        self.orientation = orientation
        self.progress_color = progress_color
        self.total = total
        self.reversed = reversed
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self._progress = 0
        self._animated_progress = 0

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value: float):
        if self.reversed:
            self._progress = self.total - value
        else:
            self._progress = value

        if self._progress > self.total:
            self._progress = self.total
        if self._progress < 0:
            self._progress = 0

    def _on_draw(self) -> None:
        inflate = Vector2()
        if self.orientation is ProgressBarOrientation.VERTICAL:
            progress = Vector2(
                self.size.x, self.size.y * self._progress / self.total
            )
            if progress.y < (self.border_radius * 2 + 2):
                inflate.x = (self.border_radius * 2 + 2) - progress.y
        else:
            progress = Vector2(
                self.size.x * self._progress / self.total, self.size.y
            )
            if progress.x < (self.border_radius * 2 + 2):
                inflate.y = (self.border_radius * 2 + 2) - progress.x
        draw.rect(
            self.context.screen,
            self.progress_color,
            Rect(
                self.world_position,
                progress,
            ).inflate(-inflate.x, -inflate.y),
            0,
            self.border_radius,
        )
        draw.rect(
            self.context.screen,
            self.border_color,
            Rect(self.world_position, self.size),
            self.border_width,
            self.border_radius,
        )
