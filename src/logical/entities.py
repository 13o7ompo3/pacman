from typing import Tuple, Optional
from src.logical.core_types import Direction, GhostState, PlayerState


class Entity:
    """Base class for movable maze entities."""

    def __init__(self, start_x: int, start_y: int) -> None:
        self.x: int = start_x
        self.y: int = start_y
        self.spawn_point: Tuple[int, int] = (start_x, start_y)

    def get_grid_position(self) -> Tuple[int, int]:
        return (self.x, self.y)


class Player(Entity):
    """Player-controlled Pac-Man state."""

    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__(start_x, start_y)
        self.lives: int = 3
        self.score: int = 0
        self.state: PlayerState = PlayerState.NORMAL
        self.gum_timer: int = 0
        self.facing: Direction = Direction.RIGHT


class Ghost(Entity):
    """Ghost state and spawn location."""

    def __init__(self, start_x: int, start_y: int, ghost_id: int = 0) -> None:
        super().__init__(start_x, start_y)
        self.ghost_id: int = ghost_id
        self.state: GhostState = GhostState.CHASE
        self.last_direction: Optional[Direction] = None
