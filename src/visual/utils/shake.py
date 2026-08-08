"""Shake effect for a node in a visual context."""

from random import randint

from pygame import Vector2

from src.visual import Context, Node


class Shake(Node):
    """Shake effect for a node in a visual context.

    Attributes:
        total_time (float): Total duration of the shake effect.
        magnitude (Vector2): Initial magnitude of the shake effect.
        acceleration (Vector2): Acceleration of the shake effect over time.

    """

    def __init__(
        self,
        context: Context,
        total_time: float,
        magnitude: Vector2,
        acceleration: Vector2,
    ) -> None:
        """Initialize the Shake effect."""
        super().__init__(context)
        self.total_time = total_time
        self.magnitude = magnitude
        self.acceleration = acceleration
        self.__delta_magnitude = magnitude
        self.__time: float = 0
        self.__target_original_position: Vector2 = Vector2()

    def apply(self) -> None:
        """Apply the shake effect to the parent node."""
        if isinstance(self.parent, Node):
            self.__time = 0
            self.__delta_magnitude = self.magnitude
            self.__target_original_position = self.parent.local_position

    def _on_update(self, delta: float) -> None:
        """Update the shake effect over time.

        Args:
            delta (float): Time elapsed since the last update.

        """
        if isinstance(self.parent, Node):
            self.__delta_magnitude += self.acceleration * delta
            if self.__time <= self.total_time:
                rand_value = Vector2()
                if int(self.__delta_magnitude.x) > 0:
                    rand_value.x = randint(
                        -int(self.__delta_magnitude.x),
                        int(self.__delta_magnitude.x),
                    )
                if int(self.__delta_magnitude.y) > 0:
                    rand_value.y = randint(
                        -int(self.__delta_magnitude.y),
                        int(self.__delta_magnitude.y),
                    )
                self.parent.local_position = (
                    self.__target_original_position + rand_value
                )

                self.__time += delta

            else:
                self.parent.local_position = self.__target_original_position
                self.__target_original_position = Vector2()
