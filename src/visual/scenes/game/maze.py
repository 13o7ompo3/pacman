from inspect import cleandoc
from pydantic import BaseModel
from pygame import KEYDOWN, Rect, Surface
import pygame
from pygame.event import Event
from pygame import draw, Color, Vector2

from src.logical.game_event import PlayerRespawnedEvent
from src.visual import Context, Node
from src.logical.maze import Direction, LogicalMaze
from src.visual.scenes.game.ghost import VisualGhost
from src.visual.scenes.game.player import Player


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


class VisualMaze(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)

        self.maze = LogicalMaze(20, 20)
        self.cell_size = 20
        wall_thickness = 3

        for x in range(self.maze.width):
            for y in range(self.maze.height):
                mask = self.maze.grid[y][x]

                cell = Cell(
                    context,
                    bool(mask & 0b0001),
                    bool(mask & 0b0010),
                    bool(mask & 0b0100),
                    bool(mask & 0b1000),
                    self.cell_size,
                    wall_thickness,
                )

                cell.local_position = Vector2(
                    self.cell_size * x,
                    self.cell_size * y,
                )

                self.add_child(cell)

        self.ghost_step_timer = 0
        self.ghost_step_duration = 0.6

        for logical_ghost in self.maze.ghosts:
            ghost = VisualGhost(
                context,
                logical_ghost,
                self.cell_size,
                self.cell_size / self.ghost_step_duration,
            )
            ghost.local_position = Vector2(self.cell_size) / 2
            self.add_child(ghost)

        self.player = Player(context, self.maze, self.cell_size)
        self.player.local_position = Vector2(self.cell_size) / 2
        self.add_child(self.player)

    def _on_update(self, delta: float) -> None:
        self.ghost_step_timer += delta
        if self.ghost_step_timer > self.ghost_step_duration:
            self.maze.tick_ghosts()
            self.ghost_step_timer = 0
        events = self.maze.tick_timers()
        for event in events:
            if isinstance(event, PlayerRespawnedEvent):
                self.player.respawn(event.x, event.y)

    def _on_draw(self) -> None:
        for x, y in self.maze.pacgums:
            draw.circle(
                self.context.screen,
                Color("#444444"),
                self.world_position
                + Vector2(self.cell_size) / 2
                + Vector2(x, y) * self.cell_size,
                2,
            )
        for x, y in self.maze.super_pacgums:
            draw.circle(
                self.context.screen,
                Color("gold"),
                self.world_position
                + Vector2(self.cell_size) / 2
                + Vector2(x, y) * self.cell_size,
                3,
            )
