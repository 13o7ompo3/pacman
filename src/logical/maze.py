from enum import Enum
from typing import Tuple
from mazegenerator import MazeGenerator
import random


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)


class GhostState(Enum):
    CHASE = "CHASE"             # Actively hunting the player
    FRIGHTENED = "FRIGHTENED"   # Blue state (running away)
    DEAD = "DEAD"               # Eaten, returning to spawn


class Entity:
    """Base class for all moving characters in the maze."""

    def __init__(self, start_x: int, start_y: int) -> None:
        self.x: int = start_x
        self.y: int = start_y
        self.direction: Direction = Direction.NONE

    def get_grid_position(self) -> Tuple[int, int]:
        """Returns the rounded grid coordinates of the entity."""
        return (self.x, self.y)


class Player(Entity):
    """Represents the player character (Pacman)."""

    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__(start_x, start_y)
        self.lives: int = 3
        self.score: int = 0


class Ghost(Entity):
    """Represents a ghost character in the maze."""

    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__(start_x, start_y)
        self.state: GhostState = GhostState.CHASE
        self.spawn_point: Tuple[int, int] = (start_x, start_y)

    def set_state(self, new_state: GhostState) -> None:
        """Sets the ghost's state."""
        self.state = new_state

    def get_target_position(self, player: Player) -> Tuple[int, int]:
        """Determines the target position for the ghost based on its state."""
        if self.state == GhostState.CHASE:
            # Pathfind towards Player
            return player.get_grid_position()
        elif self.state == GhostState.FRIGHTENED:
            self.direction = random.choice([d for d in Direction
                                            if d != Direction.NONE])
            curr_x, curr_y = self.get_grid_position()
            return (curr_x + self.direction.value[0],
                    curr_y + self.direction.value[1])
        elif self.state == GhostState.DEAD:
            # Pathfind back to self.spawn_point
            return self.spawn_point


class LogicalMaze:
    def __init__(self, width: int, height: int, seed: int = 1337,
                 pacgum: int = 42) -> None:
        self.width: int = width
        self.height: int = height
        self.pacgum: int = pacgum
        self.maze_generator: MazeGenerator = MazeGenerator((width, height),
                                                           seed=seed)
        self.grid: list[list[int]] = self.maze_generator.maze
        self.pacgum_positions: set[Tuple[int, int]] = self._place_pacgums()
        self.player = Player(start_x=width // 2, start_y=height // 2)

    def _place_pacgums(self) -> set[Tuple[int, int]]:
        """Randomly places pacgums in the maze."""
        positions: set[Tuple[int, int]] = set()
        while len(positions) < self.pacgum:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.grid[y][x] != 15:
                positions.add((x, y))
        return positions
