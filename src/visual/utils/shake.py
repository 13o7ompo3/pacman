from pygame import Vector2

from src.visual import GameComponent, Node
from random import randint


class Shake(GameComponent):
    def __init__(
        self,
        total_time: float,
        magnitude: Vector2,
        interval: float,
        decceleration: Vector2,
    ) -> None:
        self.total_time: float = total_time
        self.magnitude = magnitude
        self.interval = interval
        self.decceleration = decceleration
        self.time: float = 0
        self.target: Node | None = None
        self.target_original_position: Vector2 = Vector2()

    def apply(self, target: Node) -> None:
        self.time = 0
        self.target = target
        self.target_original_position = target.local_position

    def _on_update(self, delta: float) -> None:
        if self.target is None:
            return

        self.target.local_position = self.target_original_position + Vector2(
            randint(-int(self.magnitude.x), int(self.magnitude.x)),
            randint(-int(self.magnitude.y), int(self.magnitude.y)),
        )
        self.time += delta

        if self.time > self.total_time:
            self.time = 0
            self.target = None
            self.target.local_position = self.target_original_position
            self.target_original_position = Vector2()
