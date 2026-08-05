"""A module for visualizing a maze in a game."""

from src.visual.draw import Draw
from pygame import Surface
from pygame import Vector2
from typing import Callable

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
from src.logical.maze import LogicalMaze
from src.visual.scenes.game.ghost import VisualGhost
from src.visual.scenes.game.player import Player
from src.visual.scenes.game_over import GameOverScene, TerminalState


class Corner(Node):
    """A class representing a corner in the maze.

    Attributes:
        surface (tuple): A tuple containing the surfaces.

    """

    def __init__(
        self,
        context: Context,
        surface: tuple[Surface, Surface, Surface, Surface],
    ) -> None:
        """Initialize the Corner object."""
        super().__init__(context)
        self.surface = surface

    def _on_draw(self) -> None:
        """Draw the corner surfaces on the screen."""
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
    """A class representing the visual representation of the maze.

    Attributes:
        logical_maze (LogicalMaze): The logical representation of the maze.
        cell_size (int): The size of each cell in the maze.
        surfaces (dict): A dictionary maps corner configurations to surfaces.
        ghosts (list[VisualGhost]): A list of visual representations of ghosts.
        player (Player): The visual representation of the player.
        level_up_callback (Callable): A callback function on level up.

    """

    def __init__(
        self,
        context: Context,
        logical_maze: LogicalMaze,
        cell_size: int = 16,
        level_up_callback: Callable = lambda: None,
    ) -> None:
        """Initialize the VisualMaze object."""
        super().__init__(context)
        self.level_up_callback = level_up_callback
        self.logical_maze = logical_maze
        self.cell_size = cell_size

        self.surfaces = {
            (False, False, False, False): (
                self.context.assets.image("tile_empty_rect"),
                self.context.assets.image("tile_empty_rect"),
                self.context.assets.image("tile_empty_rect"),
                self.context.assets.image("tile_empty_rect"),
            ),
            (True, True, True, True): (
                self.context.assets.image("tile_corner_bottom_right"),
                self.context.assets.image("tile_corner_bottom_left"),
                self.context.assets.image("tile_corner_top_right"),
                self.context.assets.image("tile_corner_top_left"),
            ),
            (True, False, False, False): (
                self.context.assets.image("tile_bar_right"),
                self.context.assets.image("tile_bar_left"),
                self.context.assets.image("tile_ball_top_right"),
                self.context.assets.image("tile_ball_top_left"),
            ),
            (False, True, False, False): (
                self.context.assets.image("tile_ball_bottom_right"),
                self.context.assets.image("tile_bar_bottom"),
                self.context.assets.image("tile_ball_top_right"),
                self.context.assets.image("tile_bar_top"),
            ),
            (False, False, True, False): (
                self.context.assets.image("tile_ball_bottom_right"),
                self.context.assets.image("tile_ball_bottom_left"),
                self.context.assets.image("tile_bar_right"),
                self.context.assets.image("tile_bar_left"),
            ),
            (False, False, False, True): (
                self.context.assets.image("tile_bar_bottom"),
                self.context.assets.image("tile_ball_bottom_left"),
                self.context.assets.image("tile_bar_top"),
                self.context.assets.image("tile_ball_top_left"),
            ),
            (True, True, False, False): (
                self.context.assets.image("tile_bar_right"),
                self.context.assets.image("tile_corner_bottom_left"),
                self.context.assets.image("tile_ball_top_right"),
                self.context.assets.image("tile_bar_top"),
            ),
            (False, True, True, False): (
                self.context.assets.image("tile_ball_bottom_right"),
                self.context.assets.image("tile_bar_bottom"),
                self.context.assets.image("tile_bar_right"),
                self.context.assets.image("tile_corner_top_left"),
            ),
            (False, False, True, True): (
                self.context.assets.image("tile_bar_bottom"),
                self.context.assets.image("tile_ball_bottom_left"),
                self.context.assets.image("tile_corner_top_right"),
                self.context.assets.image("tile_bar_left"),
            ),
            (True, False, False, True): (
                self.context.assets.image("tile_corner_bottom_right"),
                self.context.assets.image("tile_bar_left"),
                self.context.assets.image("tile_bar_top"),
                self.context.assets.image("tile_ball_top_left"),
            ),
            (True, False, True, False): (
                self.context.assets.image("tile_bar_right"),
                self.context.assets.image("tile_bar_left"),
                self.context.assets.image("tile_bar_right"),
                self.context.assets.image("tile_bar_left"),
            ),
            (False, True, False, True): (
                self.context.assets.image("tile_bar_bottom"),
                self.context.assets.image("tile_bar_bottom"),
                self.context.assets.image("tile_bar_top"),
                self.context.assets.image("tile_bar_top"),
            ),
            (True, True, False, True): (
                self.context.assets.image("tile_corner_bottom_right"),
                self.context.assets.image("tile_corner_bottom_left"),
                self.context.assets.image("tile_bar_top"),
                self.context.assets.image("tile_bar_top"),
            ),
            (True, False, True, True): (
                self.context.assets.image("tile_corner_bottom_right"),
                self.context.assets.image("tile_bar_left"),
                self.context.assets.image("tile_corner_top_right"),
                self.context.assets.image("tile_bar_left"),
            ),
            (False, True, True, True): (
                self.context.assets.image("tile_bar_bottom"),
                self.context.assets.image("tile_bar_bottom"),
                self.context.assets.image("tile_corner_top_right"),
                self.context.assets.image("tile_corner_top_left"),
            ),
            (True, True, True, False): (
                self.context.assets.image("tile_bar_right"),
                self.context.assets.image("tile_corner_bottom_left"),
                self.context.assets.image("tile_bar_right"),
                self.context.assets.image("tile_corner_top_left"),
            ),
        }
        self.refresh()

    def get_surface_for_corner(
        self, cells: list[int]
    ) -> tuple[Surface, Surface, Surface, Surface]:
        """Get the surface for a corner based on the surrounding cells.

        Args:
            cells (list[int]): A list of integers of the surrounding cells.

        Returns:
            tuple: A tuple containing the surfaces for the corner

        """
        top = cells[0] & 2 | cells[1] & 8
        right = cells[1] & 4 | cells[3] & 1
        bottom = cells[2] & 2 | cells[3] & 8
        left = cells[0] & 4 | cells[2] & 1

        return self.surfaces[
            (bool(top), bool(right), bool(bottom), bool(left))
        ]

    def refresh(self):
        """Refresh the visual representation of the maze."""
        self.clear_children()
        width, height = self.logical_maze.width, self.logical_maze.height
        self.size = Vector2(width, height) * self.cell_size

        def sample_cell(x: int, y: int) -> int:
            """Sample a cell in the logical maze, 0 if out of bounds."""
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
                self.logical_maze.current_level.speed * 0.75,
            )
            ghost.local_position = Vector2(self.cell_size) / 2
            self.ghosts.append(ghost)
            self.add_child(ghost)

        self.player = Player(self.context,
                             self.logical_maze, self.cell_size,
                             self.logical_maze.current_level.speed)
        self.player.local_position = Vector2(self.cell_size) / 2
        self.add_child(self.player)

    def _on_update(self, delta: float) -> None:
        """Update the visual representation of the maze and handle events.

        Args:
            delta (float): The time elapsed since the last update.

        """
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
                if self.parent:
                    self.parent.paused = True
                self.context.root_scene.add_child(
                    GameOverScene(
                        self.context, event.final_score, TerminalState.LOST
                    )
                )
            if isinstance(event, LevelCompleteEvent):
                self.refresh()
                self.level_up_callback()
            if isinstance(event, WinEvent):
                if self.parent:
                    self.parent.paused = True
                self.context.root_scene.add_child(
                    GameOverScene(
                        self.context, event.final_score, TerminalState.WON
                    )
                )
                self.refresh()

    def _on_draw(self) -> None:
        """Draw the visual representation of the maze and pacgums."""
        for x, y in self.logical_maze.pacgums:
            Draw.circle(
                self.context.screen,
                self.world_position
                + Vector2(self.cell_size) / 2
                + Vector2(x, y) * self.cell_size,
                2,
                self.context.colors.darker,
            )
        for x, y in self.logical_maze.super_pacgums:
            Draw.circle(
                self.context.screen,
                self.world_position
                + Vector2(self.cell_size) / 2
                + Vector2(x, y) * self.cell_size,
                3,
                self.context.colors.lightest,
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
                        self.context.colors.light,
                    )
