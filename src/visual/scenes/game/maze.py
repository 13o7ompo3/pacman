from inspect import cleandoc
from src.visual.draw import Draw
from pydantic import BaseModel
from pygame import KEYDOWN, Rect, Surface
import pygame
from pygame.event import Event
from pygame import draw, Color, Vector2

from src.logical.game_event import (
    AteGhostEvent,
    GameOverEvent,
    GhostRespawnedEvent,
    PlayerDiedEvent,
    PlayerRespawnedEvent,
)
from src.visual import Context, Node
from src.logical.maze import Direction, LogicalMaze
from src.visual.scenes.game.ghost import VisualGhost
from src.visual.scenes.game.player import Player
from src.visual.scenes.game_over import GameOverScene


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
            Draw.rect(
                self.context.screen,
                self.world_position,
                Vector2(
                    self.size,
                    self.size,
                ),
                Color("crimson"),
            )
            return
        if self.left:
            Draw.rect(
                self.context.screen,
                self.world_position,
                Vector2(
                    self.wall_thickness,
                    self.size,
                ),
                Color("cyan"),
            )
        if self.top:
            Draw.rect(
                self.context.screen,
                self.world_position,
                Vector2(
                    self.size,
                    self.wall_thickness,
                ),
                Color("cyan"),
            )
        if self.right:
            Draw.rect(
                self.context.screen,
                self.world_position
                + Vector2(self.size - self.wall_thickness, 0),
                Vector2(
                    self.wall_thickness,
                    self.size,
                ),
                Color("cyan"),
            )
        if self.bottom:
            Draw.rect(
                self.context.screen,
                self.world_position
                + Vector2(0, self.size - self.wall_thickness),
                Vector2(
                    self.size,
                    self.wall_thickness,
                ),
                Color("cyan"),
            )


class VisualMaze(Node):
    def __init__(
        self,
        context: Context,
        logical_maze: LogicalMaze,
    ) -> None:
        super().__init__(context)

        width, height = logical_maze.width, logical_maze.height
        self.logical_maze = logical_maze
        self.cell_size = 20
        wall_thickness = 3
        self.size = Vector2(width, height) * self.cell_size

        for x in range(self.logical_maze.width):
            for y in range(self.logical_maze.height):
                mask = self.logical_maze.grid[y][x]

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

        self.ghosts = []
        for i, logical_ghost in enumerate(self.logical_maze.ghosts):
            ghost = VisualGhost(
                context,
                i,
                self.logical_maze,
                logical_ghost,
                self.cell_size,
                20,
            )
            ghost.local_position = Vector2(self.cell_size) / 2
            self.ghosts.append(ghost)
            self.add_child(ghost)

        self.player = Player(context, self.logical_maze, self.cell_size)
        self.player.local_position = Vector2(self.cell_size) / 2
        self.add_child(self.player)

    def _on_update(self, delta: float) -> None:
        self.logical_maze.tick_timers()
        events = self.logical_maze.flush_events()

        for event in events:
            if isinstance(event, PlayerDiedEvent):
                self.player.hidden = True
                self.player.direction = None
                self.player.next_direction = None
            if isinstance(event, PlayerRespawnedEvent):
                self.player.hidden = False
                self.player.respawn(event.x, event.y)
                for ghost in self.ghosts:
                    ghost.respawn(ghost.logical_ghost.x, ghost.logical_ghost.y)
            if isinstance(event, AteGhostEvent):
                self.ghosts[event.ghost_id].hidden = True
            if isinstance(event, GhostRespawnedEvent):
                self.ghosts[event.ghost_id].respawn(event.x, event.y)
                self.ghosts[event.ghost_id].hidden = False
            if isinstance(event, GameOverEvent):
                self.context.root_scene.add_child(
                    GameOverScene(self.context, event.final_score)
                )

    def _on_draw(self) -> None:
        for x, y in self.logical_maze.pacgums:
            Draw.circle(
                self.context.screen,
                self.world_position
                + Vector2(self.cell_size) / 2
                + Vector2(x, y) * self.cell_size,
                2,
                Color("#444444"),
            )
        for x, y in self.logical_maze.super_pacgums:
            Draw.circle(
                self.context.screen,
                self.world_position
                + Vector2(self.cell_size) / 2
                + Vector2(x, y) * self.cell_size,
                3,
                Color("gold"),
            )
