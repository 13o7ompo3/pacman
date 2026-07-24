import pygame
from src.visual.draw import Draw
from pygame.event import Event
from pygame import draw, Color, Vector2, KEYDOWN
from src.logical.core_types import PlayerState
from src.logical.game_event import PlayerDiedEvent, PlayerRespawnedEvent
from src.visual import Context, Node
from src.logical.maze import Direction, LogicalMaze


class Player(Node):
    def __init__(
        self,
        context: Context,
        maze: LogicalMaze,
        step_size: int,
        speed: float = 80,
    ) -> None:
        super().__init__(context)
        self.direction = None
        self.next_direction = None
        self.target_position = (
            Vector2(maze.player.x, maze.player.y) * step_size
        )
        self.animated_position = self.target_position.copy()
        self.step_size = step_size
        self.maze = maze
        self.speed = speed
        self.dead = False

    def _on_input(self, event: Event) -> None:
        if self.hidden:
            return
        if event.type == KEYDOWN:
            if event.key in {pygame.K_UP, pygame.K_w, pygame.K_k}:
                self.next_direction = Direction.UP
            if event.key in {pygame.K_DOWN, pygame.K_s, pygame.K_j}:
                self.next_direction = Direction.DOWN
            if event.key in {pygame.K_LEFT, pygame.K_a, pygame.K_h}:
                self.next_direction = Direction.LEFT
            if event.key in {pygame.K_RIGHT, pygame.K_d, pygame.K_l}:
                self.next_direction = Direction.RIGHT
            if self.direction is None:
                self.direction = self.next_direction

    def _on_update(self, delta: float) -> None:
        if not self.dead:
            self.animated_position = self.animated_position.move_towards(
                self.target_position, delta * self.speed
            )

        if (
            self.animated_position == self.target_position
            and self.direction is not None
        ):
            self.maze.tick_player(self.direction)
            player_pos = self.maze.player.get_grid_position()

            if self.next_direction and self.maze.can_move_player(
                self.next_direction
            ):
                self.direction = self.next_direction
                self.target_position = (
                    Vector2(player_pos) + Vector2(self.next_direction.value)
                ) * self.step_size
            else:
                self.target_position = Vector2(player_pos) * self.step_size

    def respawn(self, x, y):
        self.target_position = Vector2(x, y) * self.step_size
        self.animated_position = self.target_position.copy()

    def _on_draw(self) -> None:
        Draw.circle(
            self.context.screen,
            self.world_position + self.animated_position,
            5,
            Color("yellow"),
        )
