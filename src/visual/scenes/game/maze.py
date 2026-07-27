from inspect import cleandoc
from src.visual.draw import Draw
from pydantic import BaseModel
from pygame import KEYDOWN, Rect, Surface
import pygame
from pygame.event import Event
from pygame import draw, Color, Vector2
from typing import Dict, List, Tuple

from src.logical.game_event import (
    AteGhostEvent,
    GameOverEvent,
    GhostRespawnedEvent,
    LevelCompleteEvent,
    PlayerDiedEvent,
    PlayerRespawnedEvent,
    WinEvent,
)
from src.visual import Context, Node
from src.logical.maze import Direction, LogicalMaze
from src.visual.scenes.game.ghost import VisualGhost
from src.visual.scenes.game.player import Player
from src.visual.scenes.game_over import GameOverScene, TerminalState


class Corner(Node):
    def __init__(
        self,
        context: Context,
        surface: tuple[Surface, Surface, Surface, Surface],
    ) -> None:
        super().__init__(context)
        self.surface = surface

    def _on_draw(self) -> None:
        self.context.screen.blit(
            self.surface[0],
            self.world_position,
        )
        self.context.screen.blit(
            self.surface[1],
            self.world_position + Vector2(self.surface[0].get_width(), 0),
        )
        self.context.screen.blit(
            self.surface[2],
            self.world_position + Vector2(0, self.surface[0].get_height()),
        )
        self.context.screen.blit(
            self.surface[3],
            self.world_position
            + Vector2(
                self.surface[0].get_width(), self.surface[0].get_height()
            ),
        )


class VisualMaze(Node):
    def __init__(
        self,
        context: Context,
        logical_maze: LogicalMaze,
        cell_size: int = 16,
    ) -> None:
        super().__init__(context)
        self.logical_maze = logical_maze
        self.cell_size = cell_size

        self.surfaces = {
            (False, False, False, False): (
                pygame.image.load(
                    "assets/tiles/empty_rect.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/empty_rect.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/empty_rect.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/empty_rect.png"
                ).convert_alpha(),
            ),
            (True, True, True, True): (
                pygame.image.load(
                    "assets/tiles/corner_bottom_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_bottom_left.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_top_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_top_left.png"
                ).convert_alpha(),
            ),
            (True, False, False, False): (
                pygame.image.load(
                    "assets/tiles/bar_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_left.png").convert_alpha(),
                pygame.image.load(
                    "assets/tiles/ball_top_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/ball_top_left.png"
                ).convert_alpha(),
            ),
            (False, True, False, False): (
                pygame.image.load(
                    "assets/tiles/ball_bottom_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/bar_bottom.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/ball_top_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_top.png").convert_alpha(),
            ),
            (False, False, True, False): (
                pygame.image.load(
                    "assets/tiles/ball_bottom_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/ball_bottom_left.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/bar_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_left.png").convert_alpha(),
            ),
            (False, False, False, True): (
                pygame.image.load(
                    "assets/tiles/bar_bottom.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/ball_bottom_left.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_top.png").convert_alpha(),
                pygame.image.load(
                    "assets/tiles/ball_top_left.png"
                ).convert_alpha(),
            ),
            (True, True, False, False): (
                pygame.image.load(
                    "assets/tiles/bar_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_bottom_left.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/ball_top_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_top.png").convert_alpha(),
            ),
            (False, True, True, False): (
                pygame.image.load(
                    "assets/tiles/ball_bottom_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/bar_bottom.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/bar_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_top_left.png"
                ).convert_alpha(),
            ),
            (False, False, True, True): (
                pygame.image.load(
                    "assets/tiles/bar_bottom.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/ball_bottom_left.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_top_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_left.png").convert_alpha(),
            ),
            (True, False, False, True): (
                pygame.image.load(
                    "assets/tiles/corner_bottom_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_left.png").convert_alpha(),
                pygame.image.load("assets/tiles/bar_top.png").convert_alpha(),
                pygame.image.load(
                    "assets/tiles/ball_top_left.png"
                ).convert_alpha(),
            ),
            (True, False, True, False): (
                pygame.image.load(
                    "assets/tiles/bar_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_left.png").convert_alpha(),
                pygame.image.load(
                    "assets/tiles/bar_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_left.png").convert_alpha(),
            ),
            (False, True, False, True): (
                pygame.image.load(
                    "assets/tiles/bar_bottom.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/bar_bottom.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_top.png").convert_alpha(),
                pygame.image.load("assets/tiles/bar_top.png").convert_alpha(),
            ),
            (True, True, False, True): (
                pygame.image.load(
                    "assets/tiles/corner_bottom_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_bottom_left.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_top.png").convert_alpha(),
                pygame.image.load("assets/tiles/bar_top.png").convert_alpha(),
            ),
            (True, False, True, True): (
                pygame.image.load(
                    "assets/tiles/corner_bottom_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_left.png").convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_top_right.png"
                ).convert_alpha(),
                pygame.image.load("assets/tiles/bar_left.png").convert_alpha(),
            ),
            (False, True, True, True): (
                pygame.image.load(
                    "assets/tiles/bar_bottom.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/bar_bottom.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_top_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_top_left.png"
                ).convert_alpha(),
            ),
            (True, True, True, False): (
                pygame.image.load(
                    "assets/tiles/bar_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_bottom_left.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/bar_right.png"
                ).convert_alpha(),
                pygame.image.load(
                    "assets/tiles/corner_top_left.png"
                ).convert_alpha(),
            ),
        }
        self.refresh()

    def get_surface_for_corner(
        self, cells: list[int]
    ) -> tuple[Surface, Surface, Surface, Surface]:
        top = cells[0] & 2 | cells[1] & 8
        right = cells[1] & 4 | cells[3] & 1
        bottom = cells[2] & 2 | cells[3] & 8
        left = cells[0] & 4 | cells[2] & 1

        return self.surfaces[
            (bool(top), bool(right), bool(bottom), bool(left))
        ]

    def refresh(self):
        self.clear_children()
        width, height = self.logical_maze.width, self.logical_maze.height
        self.size = Vector2(width, height) * self.cell_size

        def sample_cell(x: int, y: int) -> int:
            if x < 0 and y < 0:
                return 0
            if x < 0 and y >= height:
                return 0
            if x >= width and y < 0:
                return 0
            if x < 0:
                return self.logical_maze.grid[y][0] & 8
            if y < 0:
                return self.logical_maze.grid[0][x] & 1
            if x >= width and y >= height:
                return 0
            if x >= width:
                return self.logical_maze.grid[y][width - 1] & 2
            if y >= height:
                return self.logical_maze.grid[height - 1][x] & 4
            return self.logical_maze.grid[y][x]

        for x in range(-1, self.logical_maze.width):
            for y in range(-1, self.logical_maze.height):
                cells = [
                    sample_cell(x, y),
                    sample_cell(x + 1, y),
                    sample_cell(x, y + 1),
                    sample_cell(x + 1, y + 1),
                ]

                corner = Corner(
                    self.context, self.get_surface_for_corner(cells)
                )

                corner.local_position = Vector2(
                    self.cell_size * (x + 0.5),
                    self.cell_size * (y + 0.5),
                )

                self.add_child(corner)

        self.ghosts = []
        for i, logical_ghost in enumerate(self.logical_maze.ghosts):
            ghost = VisualGhost(
                self.context,
                i,
                self.logical_maze,
                logical_ghost,
                self.cell_size,
                20,
            )
            ghost.local_position = Vector2(self.cell_size) / 2
            self.ghosts.append(ghost)
            self.add_child(ghost)

        self.player = Player(self.context, self.logical_maze, self.cell_size)
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
                    GameOverScene(
                        self.context, event.final_score, TerminalState.LOST
                    )
                )
            if isinstance(event, LevelCompleteEvent):
                self.refresh()
            if isinstance(event, WinEvent):
                self.context.root_scene.add_child(
                    GameOverScene(
                        self.context, event.final_score, TerminalState.WON
                    )
                )
                self.refresh()

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

        ft_small = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]
        posy = int((self.logical_maze.height - len(ft_small)) / 2)
        posx = int((self.logical_maze.width - len(ft_small[0])) / 2)
        for y in range(len(ft_small)):
            for x in range(len(ft_small[0])):
                if ft_small[y][x] == 1:
                    Draw.rect(
                        self.context.screen,
                        self.world_position
                        + Vector2(posx + x, posy + y) * self.cell_size,
                        Vector2(self.cell_size, self.cell_size),
                        Color("#bf53c9"),
                    )
