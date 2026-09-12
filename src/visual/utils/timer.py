"""Define a timer component."""

from typing import Callable
from src.visual import GameComponent


class Timer(GameComponent):
    """A timer component that triggers a callback after a specified time.

    Attributes:
        time (float): The time in seconds after which the callback is triggered.
        on_finish (Callable): The callback function to be called when the timer finishes.
        repeating (bool): Whether the timer should repeat after finishing.
        counting (bool): Whether the timer is currently counting down.
        elapsed (float): The elapsed time since the timer started.

    """

    def __init__(
        self,
        time: float,
        on_finish: Callable,
        on_start: Callable = lambda _: None,
        repeating: bool = False,
    ) -> None:
        """Initialize the timer component."""
        super().__init__()
        self.time = time
        self.on_start = on_start
        self.on_finish = on_finish
        self.repeating = repeating
        self.counting = False
        self.elapsed: float = 0

    def start(self) -> None:
        """Start the timer."""
        self.on_start(self)
        self.elapsed: float = 0
        self.counting = True

    def stop(self) -> None:
        """Stop the timer."""
        self.counting = False

    def _on_update(self, delta: float) -> None:
        """Update the timer.

        Args:
            delta (float): The time in seconds since the last update.
        """
        if not self.counting:
            return

        self.elapsed += delta

        if self.elapsed >= self.time:
            self.on_finish(self)
            self.elapsed = 0
            if not self.repeating:
                self.counting = False
