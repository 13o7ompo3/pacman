from src.logical.entities import Ghost
from src.logical.maze import LogicalMaze
from src.visual import Node, Context
from pygame import draw, Color, Vector2


class VisualGhost(Node):
    def __init__(
        self, context: Context, ghost: Ghost, step_size: int, speed: float
    ) -> None:
        super().__init__(context)
        self.logical_ghost = ghost
        self.step_size = step_size
        self.target_position = Vector2(ghost.x, ghost.y) * step_size
        self.animated_position = self.target_position.copy()
        self.speed = speed

    def _on_update(self, delta: float) -> None:
        self.target_position = (
            Vector2(self.logical_ghost.x, self.logical_ghost.y)
            * self.step_size
        )
        self.animated_position = self.animated_position.move_towards(
            self.target_position, self.speed * delta
        )

    def _on_draw(self) -> None:
        draw.circle(
            self.context.screen,
            Color("blue"),
            self.world_position + self.animated_position,
            4,
        )
