from pydantic import BaseModel
from pygame import KEYDOWN, Rect, Surface
import pygame
from pygame.event import Event
from pygame import draw, Color, Vector2

from src.visual import Context, Node
from src.logical.maze import Direction, LogicalMaze


class Cell(Node):
    def __init__(
        self,
        context: Context,
        top: bool,
        right: bool,
        bottom: bool,
        left: bool,
        size: int,
        wall_thickness: int,
    ) -> None:
        super().__init__(context)
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

        self.size = size
        self.wall_thickness = wall_thickness

        self.maze = LogicalMaze(20, 20)

    def _on_draw(self) -> None:
        if self.left and self.right and self.top and self.bottom:
            draw.rect(
                self.context.screen,
                Color("crimson"),
                Rect(
                    self.world_position,
                    Vector2(
                        self.size,
                        self.size,
                    ),
                ),
            )
            return
        if self.left:
            draw.rect(
                self.context.screen,
                Color("cyan"),
                Rect(
                    self.world_position,
                    Vector2(
                        self.wall_thickness,
                        self.size,
                    ),
                ),
            )
        if self.top:
            draw.rect(
                self.context.screen,
                Color("cyan"),
                Rect(
                    self.world_position,
                    Vector2(
                        self.size,
                        self.wall_thickness,
                    ),
                ),
            )
        if self.right:
            draw.rect(
                self.context.screen,
                Color("cyan"),
                Rect(
                    self.world_position
                    + Vector2(self.size - self.wall_thickness, 0),
                    Vector2(
                        self.wall_thickness,
                        self.size,
                    ),
                ),
            )
        if self.bottom:
            draw.rect(
                self.context.screen,
                Color("cyan"),
                Rect(
                    self.world_position
                    + Vector2(0, self.size - self.wall_thickness),
                    Vector2(
                        self.size,
                        self.wall_thickness,
                    ),
                ),
            )


class Player(Node):
    # enum Direction
    def __init__(
        self,
        context: Context,
        maze: LogicalMaze,
        step_size: int,
        speed: int = 200,
    ) -> None:
        super().__init__(context)
        self.direction = None
        self.target_position = self.world_position
        self.animated_position = self.world_position
        self.step_size = step_size
        self.maze = maze
        self.speed = speed

    def _on_input(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key in {pygame.K_UP, pygame.K_w, pygame.K_k}:
                self.direction = Direction.UP
            if event.key in {pygame.K_DOWN, pygame.K_s, pygame.K_j}:
                self.direction = Direction.DOWN
            if event.key in {pygame.K_LEFT, pygame.K_a, pygame.K_h}:
                self.direction = Direction.LEFT
            if event.key in {pygame.K_RIGHT, pygame.K_d, pygame.K_l}:
                self.direction = Direction.RIGHT

            if self.direction is not None:
                _ = self.maze.tick_player(self.direction)
                x, y = self.maze.player.get_grid_position()
                print(x, y)
                self.target_position = Vector2(
                    x * self.step_size,
                    y * self.step_size,
                )

    def _on_update(self, delta: float) -> None:
        self.animated_position = self.animated_position.move_towards(
            self.target_position, delta * self.speed
        )
        if (
            self.animated_position == self.target_position
            and self.direction is not None
        ):
            _ = self.maze.tick_player(self.direction)
            x, y = self.maze.player.get_grid_position()
            print(x, y)
            self.target_position = Vector2(
                x * self.step_size,
                y * self.step_size,
            )

    def _on_draw(self) -> None:
        draw.circle(
            self.context.screen,
            Color("yellow"),
            self.world_position + self.animated_position,
            5,
            False,
        )


class VisualMaze(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)

        self.local_position = Vector2(100, 100)
        self.maze = LogicalMaze(20, 20)
        cell_size = 20
        wall_thickness = 3

        for x in range(len(self.maze.grid)):
            for y in range(len(self.maze.grid[x])):
                mask = self.maze.grid[y][x]

                cell = Cell(
                    context,
                    bool(mask & 0b0001),
                    bool(mask & 0b0010),
                    bool(mask & 0b0100),
                    bool(mask & 0b1000),
                    cell_size,
                    wall_thickness,
                )

                cell.local_position = Vector2(
                    cell_size * x,
                    cell_size * y,
                )

                self.add_child(cell)

        self.player = Player(context, self.maze, cell_size)
        self.player.local_position = Vector2(cell_size) / 2
        self.add_child(self.player)
