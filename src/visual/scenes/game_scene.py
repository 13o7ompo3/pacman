from pydantic import BaseModel
from pygame import KEYDOWN, Rect, Surface
import pygame
from pygame.event import Event
from pygame import draw, Color, Vector2

from src.visual import Context, Node
from src.logical.maze import LogicalMaze


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
    def __init__(
        self, context: Context, step_size: int, maze: LogicalMaze
    ) -> None:
        super().__init__(context)
        self.position = (0, 0)
        self.step_size = step_size
        self.maze = maze

    def _on_input(self, event: Event) -> None:
        x, y = self.position
        new_pos = (0, 0)
        if event.type == KEYDOWN:
            if event.key in {pygame.K_UP, pygame.K_w}:
                new_pos = (x, y - 1)
                if self.maze.can_move(self.position, new_pos):
                    self.local_position.y -= self.step_size
            if event.key in {pygame.K_DOWN, pygame.K_s}:
                new_pos = (x, y + 1)
                if self.maze.can_move(self.position, new_pos):
                    self.local_position.y += self.step_size
            if event.key in {pygame.K_LEFT, pygame.K_a}:
                new_pos = (x - 1, y)
                if self.maze.can_move(self.position, new_pos):
                    self.local_position.x -= self.step_size
            if event.key in {pygame.K_RIGHT, pygame.K_d}:
                new_pos = (x + 1, y)
                if self.maze.can_move(self.position, new_pos):
                    self.local_position.x += self.step_size
        self.position = new_pos

    def _on_draw(self) -> None:
        draw.circle(
            self.context.screen, Color("yellow"), self.world_position, 5
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

        self.player = Player(context, cell_size, self.maze)
        self.player.local_position = Vector2(cell_size) / 2
        self.add_child(self.player)
