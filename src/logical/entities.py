from typing import Tuple, Optional
from src.logical.core_types import Direction, GhostState, PlayerState


class Entity:
    """Base class for movable maze entities."""

    def __init__(self, start_x: int, start_y: int) -> None:
        """Initialize the entity's position and spawn point.

        Args:
            start_x (int): The starting x-coordinate of the entity.
            start_y (int): The starting y-coordinate of the entity.

        Returns:
            None
        """
        self.x: int = start_x
        self.y: int = start_y
        self.spawn_point: Tuple[int, int] = (start_x, start_y)

    def get_grid_position(self) -> Tuple[int, int]:
        """Get the current grid position of the entity.

        Args:
            None

        Returns:
            Tuple[int, int]: The current (x, y) position of the entity.
        """
        return (self.x, self.y)


class Player(Entity):
    """Player-controlled Pac-Man state."""

    def __init__(self, start_x: int, start_y: int) -> None:
        """Initialize the player's position and initial state.

        Args:
            start_x (int): The starting x-coordinate of the player.
            start_y (int): The starting y-coordinate of the player.

        Returns:
            None
        """
        super().__init__(start_x, start_y)
        self.lives: int = 3
        self.score: int = 0
        self.state: PlayerState = PlayerState.NORMAL
        self.gum_timer: int = 0
        self.facing: Direction = Direction.RIGHT


class Ghost(Entity):
    """Ghost state and spawn location."""

    def __init__(self, start_x: int, start_y: int, ghost_id: int = 0) -> None:
        """Initialize the ghost's position, state, and unique identifier.

        Args:
            start_x (int): The starting x-coordinate of the ghost.
            start_y (int): The starting y-coordinate of the ghost.
            ghost_id (int): Unique identifier for the ghost.

        Returns:
            None
        """
        super().__init__(start_x, start_y)
        self.ghost_id: int = ghost_id
        self.state: GhostState = GhostState.CHASE
        self.last_direction: Optional[Direction] = None
        self.next_move: Optional[Direction] = None
