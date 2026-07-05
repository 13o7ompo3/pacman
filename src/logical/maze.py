from enum import Enum
from typing import Tuple, List, Literal, TypeAlias
from mazegenerator import MazeGenerator
import random


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)


Moves: TypeAlias = List[Literal[Direction.DOWN, Direction.UP,
                                Direction.LEFT, Direction.RIGHT]]


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
                 super_pacgum: int = 42) -> None:
        self.width: int = width
        self.height: int = height
        self.super_pacgum: int = super_pacgum
        self.maze_generator: MazeGenerator = MazeGenerator((width, height),
                                                           seed=seed)
        self.grid: list[list[int]] = self.maze_generator.maze
        self.super_pacgums: set[Tuple[int, int]] = self._place_super_pacgums()
        self.pacgums: set[Tuple[int, int]] = self._place_pacgums()
        self.ghosts: list[Ghost] = self._initialize_ghosts()
        self.player = Player(start_x=width // 2, start_y=height // 2)

    def _initialize_ghosts(self) -> list[Ghost]:
        """Initializes ghosts at predefined positions."""
        ghost_positions = [(1, 1), (self.width - 2, 1),
                           (1, self.height - 2),
                           (self.width - 2, self.height - 2)]
        return [Ghost(x, y) for x, y in ghost_positions]

    def _place_super_pacgums(self) -> set[Tuple[int, int]]:
        """Randomly places super pacgums in the maze."""
        positions: set[Tuple[int, int]] = set()
        while len(positions) < self.super_pacgum:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.grid[y][x] != 15:
                positions.add((x, y))
        return positions

    def _place_pacgums(self) -> set[Tuple[int, int]]:
        """Places pacgums in all empty cells of the maze."""
        positions: set[Tuple[int, int]] = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != 15 and (x, y) not in self.super_pacgums:
                    positions.add((x, y))
        return positions

    def can_move(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
        """Checks if the player can move from p1 to p2."""
        x1, y1 = p1
        x2, y2 = p2

        # Check if the destination is within the maze bounds
        if not (0 <= x2 < self.width and 0 <= y2 < self.height):
            return False

        # Check if the movement is valid (adjacent cells)
        if abs(x2 - x1) + abs(y2 - y1) != 1:
            return False

        # Check if there's a wall between the two cells
        dx = x2 - x1
        dy = y2 - y1
        direction_to_wall = {
            Direction.UP.value: 1,
            Direction.DOWN.value: 2,
            Direction.LEFT.value: 4,
            Direction.RIGHT.value: 8
        }
        if direction_to_wall.get((dx, dy), 0) & self.grid[y1][x1]:
            return False

        return True

    def move_player(self, direction: Direction) -> bool:
        """Attempts to move the player in the specified direction."""
        dx, dy = direction.value
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if self.can_move((self.player.x, self.player.y), (new_x, new_y)):
            self.player.x = new_x
            self.player.y = new_y
            return True
        return False

    def available_moves(self, position: Tuple[int, int]
                        ) -> Moves:
        """Returns a list of available directions the player can move to."""
        moves = []
        for direction in Direction:
            if direction == Direction.NONE:
                continue
            dx, dy = direction.value
            new_x = position[0] + dx
            new_y = position[1] + dy
            if self.can_move(position, (new_x, new_y)):
                moves.append(direction)
        return moves

    def _move_ghost(self, ghost: Ghost, player: Player) -> None:
        """Moves the ghost towards its target position based on its state."""
        target_x, target_y = ghost.get_target_position(player)
        current_x, current_y = ghost.get_grid_position()

        # Determine the best direction to move towards the target
        best_direction = Direction.NONE
        min_distance = float('inf')

        for direction in Direction:
            if direction == Direction.NONE:
                continue
            dx, dy = direction.value
            new_x = current_x + dx
            new_y = current_y + dy

            if self.can_move((current_x, current_y), (new_x, new_y)):
                distance = abs(new_x - target_x) + abs(new_y - target_y)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction

        # Move the ghost in the best direction found
        if best_direction != Direction.NONE:
            ghost.x += best_direction.value[0]
            ghost.y += best_direction.value[1]

    def move_ghosts(self) -> None:
        """Moves all ghosts based on their current state."""
        for ghost in self.ghosts:
            self._move_ghost(ghost, self.player)
