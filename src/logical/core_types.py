from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Direction(Enum):
    """Orthogonal movement directions in the maze."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)


class GhostState(Enum):
    """Behavioral state for a ghost."""

    CHASE = "CHASE"
    FRIGHTENED = "FRIGHTENED"
    DEAD = "DEAD"


class PlayerState(Enum):
    """Current player state."""

    NORMAL = "NORMAL"
    POWERED_UP = "POWERED_UP"
    DEAD = "DEAD"


class TickEvent(Enum):
    """Events emitted by a single simulation tick."""

    NONE = "NONE"
    ATE_PACGUM = "ATE_PACGUM"
    ATE_SUPER_PACGUM = "ATE_SUPER_PACGUM"
    ATE_GHOST = "ATE_GHOST"
    GHOST_RESPAWNED = "GHOST_RESPAWNED"
    PLAYER_DIED = "PLAYER_DIED"
    PLAYER_RESPAWNED = "PLAYER_RESPAWNED"
    GAME_OVER = "GAME_OVER"
    LEVEL_COMPLETE = "LEVEL_COMPLETE"
    TIME_UP = "TIME_UP"


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
