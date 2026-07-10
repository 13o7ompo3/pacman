import logging
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, List, Optional
from mazegenerator import MazeGenerator  # type: ignore[import-not-found]

logger = logging.getLogger(__name__)


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
    PLAYER_DIED = "PLAYER_DIED"
    GAME_OVER = "GAME_OVER"
    LEVEL_COMPLETE = "LEVEL_COMPLETE"
    TIME_UP = "TIME_UP"


class Entity:
    """Base class for movable maze entities."""

    def __init__(self, start_x: int, start_y: int) -> None:
        """Create an entity at the given grid position."""
        self.x: int = start_x
        self.y: int = start_y
        self.spawn_point: Tuple[int, int] = (start_x, start_y)

    def get_grid_position(self) -> Tuple[int, int]:
        """Return the entity's current grid position."""
        return (self.x, self.y)


class Player(Entity):
    """Player-controlled Pac-Man state."""

    def __init__(self, start_x: int, start_y: int) -> None:
        """Create a player at the given start position."""
        super().__init__(start_x, start_y)
        self.lives: int = 3
        self.score: int = 0
        self.state: PlayerState = PlayerState.NORMAL
        self.gum_timer: int = 0
        self.facing: Direction = Direction.RIGHT


class Ghost(Entity):
    """Ghost state and spawn location."""

    def __init__(self, start_x: int, start_y: int, ghost_id: int = 0) -> None:
        """Create a ghost at the given start position."""
        super().__init__(start_x, start_y)
        self.ghost_id: int = ghost_id
        self.state: GhostState = GhostState.CHASE
        self.last_direction: Optional[Direction] = None


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


class LogicalMaze:
    """Encapsulate maze generation, movement, and collision rules."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int = 1337,
        player: Optional[Player] = None,
        points_pacgum: int = 10,
        points_super_pacgum: int = 50,
        points_ghost: int = 200,
        max_ticks: int = 90 * 60,
        super_pacgum_duration: int = 600,
    ) -> None:
        """Create a new logical maze with a fresh entity layout."""
        self.width: int = width
        self.height: int = height
        self.points_pacgum: int = points_pacgum
        self.points_super_pacgum: int = points_super_pacgum
        self.points_ghost: int = points_ghost
        self.max_ticks: int = max_ticks
        self.elapsed_ticks: int = 0
        self.super_pacgum_duration: int = super_pacgum_duration
        self.cheat_invincible: bool = False
        self.cheat_freeze_ghosts: bool = False

        self.maze_generator = MazeGenerator((width, height), seed=seed)
        self.grid: list[list[int]] = self.maze_generator.maze

        self.player = player if player else Player(width // 2, height // 2)
        self.player.x, self.player.y = width // 2, height // 2
        self.player.state = PlayerState.NORMAL

        self.ghosts: list[Ghost] = self._initialize_ghosts()
        self.super_pacgums: set[Tuple[int, int]] = self._place_super_pacgums()
        self.pacgums: set[Tuple[int, int]] = self._place_pacgums()

    def _initialize_ghosts(self) -> list[Ghost]:
        """Place ghosts in their four corner spawn points."""
        # 4 corners per PDF specification
        positions = [
            (1, 1),
            (self.width - 2, 1),
            (1, self.height - 2),
            (self.width - 2, self.height - 2)
        ]
        return [
            Ghost(x, y, ghost_id=index)
            for index, (x, y) in enumerate(positions)
        ]

    def _place_super_pacgums(self) -> set[Tuple[int, int]]:
        """Place power pellets at the designated corner positions."""
        positions: set[Tuple[int, int]] = set()
        corners = [
            (1, 1),
            (self.width - 2, 1),
            (1, self.height - 2),
            (self.width - 2, self.height - 2)
        ]
        for cx, cy in corners:
            if self.grid[cy][cx] != 15:
                positions.add((cx, cy))
        return positions

    def _place_pacgums(self) -> set[Tuple[int, int]]:
        """Place normal pellets on every non-wall cell except the spawn
        tile."""
        positions: set[Tuple[int, int]] = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != 15 and (x, y) not in self.super_pacgums:
                    positions.add((x, y))
        # Do not spawn pacgum on player start
        positions.discard(self.player.get_grid_position())
        return positions

    @property
    def is_level_complete(self) -> bool:
        """Return whether all pellets and power pellets have been eaten."""
        return not self.pacgums and not self.super_pacgums

    @property
    def is_game_over(self) -> bool:
        """Return True when the player has no lives remaining."""
        return self.player.lives <= 0

    @property
    def ticks_remaining(self) -> int:
        """Return the number of ticks remaining before the time limit."""
        return max(0, self.max_ticks - self.elapsed_ticks)

    @property
    def is_time_up(self) -> bool:
        """Return True when the level timer has expired."""
        return self.elapsed_ticks >= self.max_ticks

    def can_move(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
        """Check whether an entity can move from p1 to p2.

        p2 must be orthogonally adjacent to p1 and in-bounds; returns False
        otherwise. Intended for single-step moves, not pathfinding.
        """
        x1, y1 = p1
        x2, y2 = p2

        if not (0 <= x2 < self.width and 0 <= y2 < self.height):
            return False
        if abs(x2 - x1) + abs(y2 - y1) != 1:
            return False

        dx, dy = x2 - x1, y2 - y1
        direction_to_wall = {
            Direction.UP.value: 1,
            Direction.RIGHT.value: 2,
            Direction.DOWN.value: 4,
            Direction.LEFT.value: 8
        }
        if direction_to_wall.get((dx, dy), 0) & self.grid[y1][x1]:
            return False
        return True

    def _get_valid_moves(
            self, current_pos: Tuple[int, int]) -> List[Direction]:
        """Return the legal orthogonal moves from the current position."""
        valid_moves: List[Direction] = []
        for direction in Direction:
            if direction == Direction.NONE:
                continue
            nx = current_pos[0] + direction.value[0]
            ny = current_pos[1] + direction.value[1]
            if self.can_move(current_pos, (nx, ny)):
                valid_moves.append(direction)
        return valid_moves

    def _move_ghost(self, ghost: Ghost) -> None:
        """Advance a ghost by one step using its current chase behavior."""
        valid_moves = self._get_valid_moves(ghost.get_grid_position())
        if not valid_moves:
            logger.warning(
                "Ghost at %s has no valid moves",
                ghost.get_grid_position(),
            )
            return

        px, py = self.player.get_grid_position()
        best_dir = valid_moves[0]
        reverse_direction = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        candidates = [
            direction
            for direction in valid_moves
            if ghost.last_direction is None
            or direction != reverse_direction.get(ghost.last_direction)
        ] or valid_moves

        if ghost.state == GhostState.CHASE:
            best_dir = min(
                candidates,
                key=lambda d: abs((ghost.x + d.value[0]) - px)
                + abs((ghost.y + d.value[1]) - py),
            )
        elif ghost.state == GhostState.FRIGHTENED:
            best_dir = max(
                candidates,
                key=lambda d: abs((ghost.x + d.value[0]) - px)
                + abs((ghost.y + d.value[1]) - py),
            )
        elif ghost.state == GhostState.DEAD:
            sx, sy = ghost.spawn_point
            best_dir = min(
                candidates,
                key=lambda d: abs((ghost.x + d.value[0]) - sx)
                + abs((ghost.y + d.value[1]) - sy),
            )

        ghost.x += best_dir.value[0]
        ghost.y += best_dir.value[1]
        ghost.last_direction = best_dir

        if (ghost.state == GhostState.DEAD
           and ghost.get_grid_position() == ghost.spawn_point):
            ghost.state = GhostState.CHASE
            ghost.last_direction = None

    def level_skip(self) -> None:
        """Cheat: immediately clear all pellets to complete the level."""
        self.pacgums.clear()
        self.super_pacgums.clear()

    def respawn_player(self) -> None:
        """Reset the player and ghosts after a death.

        This preserves the current pellets and power pellets.
        """
        self.player.x, self.player.y = self.width // 2, self.height // 2
        self.player.state = PlayerState.NORMAL
        self.player.facing = Direction.RIGHT
        self.player.gum_timer = 0

        for ghost in self.ghosts:
            ghost.x, ghost.y = ghost.spawn_point
            ghost.state = GhostState.CHASE
            ghost.last_direction = None

    def get_render_state(self) -> RenderState:
        """Return a read-only snapshot of the current render state."""
        return RenderState(
            player_x=self.player.x,
            player_y=self.player.y,
            player_state=self.player.state,
            player_facing=self.player.facing,
            player_lives=self.player.lives,
            player_score=self.player.score,
            ghosts=tuple(
                (ghost.x, ghost.y, ghost.state, ghost.ghost_id)
                for ghost in self.ghosts
            ),
            pacgums=frozenset(self.pacgums),
            super_pacgums=frozenset(self.super_pacgums),
            ticks_remaining=self.ticks_remaining,
            is_level_complete=self.is_level_complete,
            is_game_over=self.is_game_over,
            time_up=self.is_time_up,
        )

    def _resolve_collisions(self) -> List[TickEvent]:
        """Apply item and entity collisions and return emitted events."""
        events: List[TickEvent] = []
        p_pos = self.player.get_grid_position()

        # Items
        if p_pos in self.pacgums:
            self.pacgums.remove(p_pos)
            self.player.score += self.points_pacgum
            events.append(TickEvent.ATE_PACGUM)
        elif p_pos in self.super_pacgums:
            self.super_pacgums.remove(p_pos)
            self.player.score += self.points_super_pacgum
            self.player.gum_timer = self.super_pacgum_duration
            self.player.state = PlayerState.POWERED_UP
            events.append(TickEvent.ATE_SUPER_PACGUM)
            for ghost in self.ghosts:
                if ghost.state != GhostState.DEAD:
                    ghost.state = GhostState.FRIGHTENED
                    ghost.last_direction = None

        # Entities
        for ghost in self.ghosts:
            if ghost.get_grid_position() == p_pos:
                if (
                    ghost.state == GhostState.CHASE
                    and not self.cheat_invincible
                ):
                    self.player.lives -= 1
                    self.player.state = PlayerState.DEAD
                    if self.player.lives <= 0:
                        events.append(TickEvent.GAME_OVER)
                    else:
                        events.append(TickEvent.PLAYER_DIED)
                    break
                elif ghost.state == GhostState.FRIGHTENED:
                    ghost.state = GhostState.DEAD
                    ghost.last_direction = None
                    self.player.score += self.points_ghost
                    events.append(TickEvent.ATE_GHOST)

        if self.is_level_complete:
            events.append(TickEvent.LEVEL_COMPLETE)

        return events

    def tick_player(self, player_dir: Direction) -> List[TickEvent]:
        """Move the player one step and resolve collisions.

        Call this at whatever rate the player should move.
        The caller (view) is responsible for timing.

        Args:
            player_dir: The direction input for this step.

        Returns:
            List of TickEvents that occurred this step.
        """
        events: List[TickEvent] = []

        if self.player.state == PlayerState.DEAD:
            return events

        # Move
        if player_dir != Direction.NONE:
            nx = self.player.x + player_dir.value[0]
            ny = self.player.y + player_dir.value[1]
            if self.can_move((self.player.x, self.player.y), (nx, ny)):
                self.player.x, self.player.y = nx, ny
                self.player.facing = player_dir

        # Collisions after every move
        events.extend(self._resolve_collisions())
        return events

    def tick_ghosts(self) -> List[TickEvent]:
        """Move all ghosts one step and resolve collisions.

        Call this at whatever rate ghosts should move.
        The caller (view) is responsible for timing.

        Returns:
            List of TickEvents that occurred this step.
        """
        events: List[TickEvent] = []

        if self.player.state == PlayerState.DEAD:
            return events

        if not self.cheat_freeze_ghosts:
            for ghost in self.ghosts:
                self._move_ghost(ghost)

        events.extend(self._resolve_collisions())
        return events

    def tick_timers(self) -> List[TickEvent]:
        """Advance all time-based state by one frame.

        Call this every tick regardless of player/ghost speed.
        Handles the power-up countdown and the level time limit.

        Returns:
            List of TickEvents that occurred this frame.
        """
        events: List[TickEvent] = []

        self.elapsed_ticks += 1

        # Power-up countdown
        if self.player.gum_timer > 0:
            self.player.gum_timer -= 1
            if self.player.gum_timer <= 0:
                self.player.state = PlayerState.NORMAL
                for ghost in self.ghosts:
                    if ghost.state == GhostState.FRIGHTENED:
                        ghost.state = GhostState.CHASE

        # Level time limit
        if self.is_time_up:
            events.append(TickEvent.TIME_UP)

        return events
