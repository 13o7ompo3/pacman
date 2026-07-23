from src.logical.entities import Ghost
from src.visual.draw import Draw
from src.logical.game_event import AteGhostEvent
from src.logical.maze import LogicalMaze
from src.visual import Node, Context
from pygame import draw, Color, Vector2


class VisualGhost(Node):
    def __init__(
        self,
        context: Context,
        id: int,
        maze: LogicalMaze,
        ghost: Ghost,
        step_size: int,
        speed: float,
    ) -> None:
        super().__init__(context)
        self.id = id
        self.logical_maze = maze
        self.logical_ghost = ghost
        self.step_size = step_size
        self.target_position = Vector2(ghost.x, ghost.y) * step_size
        self.animated_position = self.target_position.copy()

        self.ghost_step_timer = 0
        self.speed = speed
        self.ghost_step_duration = step_size / self.speed

    def _on_update(self, delta: float) -> None:
        self.ghost_step_timer += delta
        if self.ghost_step_timer > self.ghost_step_duration:
            self.logical_maze.tick_ghost(self.id)
            self.ghost_step_timer = 0

        self.target_position = (
            Vector2(self.logical_ghost.x, self.logical_ghost.y)
            * self.step_size
        )
        self.animated_position = self.animated_position.move_towards(
            self.target_position, self.speed * delta
        )

    def _on_draw(self) -> None:
        Draw.circle(
            self.context.screen,
            self.world_position + self.animated_position,
            4,
            Color("blue"),
        )

    def respawn(self, x, y):
        self.target_position = Vector2(x, y) * self.step_size
        self.animated_position = self.target_position.copy()
        self.dead = False
