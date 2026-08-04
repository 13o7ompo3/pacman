from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Direction(Enum):
    """Orthogonal movement directions in the maze.

    Attributes:
        UP: Move up in the maze.
        DOWN: Move down in the maze.
        LEFT: Move left in the maze.
        RIGHT: Move right in the maze.
        NONE: Do not move.
    """

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)


class GhostState(Enum):
    """Behavioral state for a ghost.

    Attributes:
        CHASE: The ghost is chasing the player.
        FRIGHTENED: The ghost is frightened and can be eaten by the player.
        DEAD: The ghost has been eaten by the player
    """

    CHASE = "CHASE"
    FRIGHTENED = "FRIGHTENED"
    DEAD = "DEAD"


class PlayerState(Enum):
    """Current player state.

    Attributes:
        NORMAL: The player is in the normal state.
        POWERED_UP: The player has eaten a super pacgum.
        DEAD: The player has been eaten by a ghost and is dead.
    """

    NORMAL = "NORMAL"
    POWERED_UP = "POWERED_UP"
    DEAD = "DEAD"


@dataclass(frozen=True)
class RenderState:
    """Read-only snapshot of everything the renderer needs per frame."""

    player_x: int
    player_y: int
    player_state: PlayerState
    player_facing: Direction
    player_lives: int
    player_score: int
    ghosts: tuple[tuple[int, int, GhostState, int], ...]
    pacgums: frozenset[Tuple[int, int]]
    super_pacgums: frozenset[Tuple[int, int]]
    ticks_remaining: int
    is_level_complete: bool
    is_game_over: bool
    time_up: bool
