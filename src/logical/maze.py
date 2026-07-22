import logging
from typing import Tuple, List, Optional, Set
from mazegenerator import MazeGenerator  # type: ignore[import-not-found]
from src.logical.core_types import (
    Direction,
    GhostState,
    PlayerState,
    RenderState
)
from src.logical.game_event import (
    GameEvent,
    AtePacgumEvent,
    AteSuperPacgumEvent,
    AteGhostEvent,
    PlayerDiedEvent,
    PlayerRespawnedEvent,
    GhostRespawnedEvent,
    PowerUpExpiredEvent,
    LevelCompleteEvent,
    GameOverEvent,
    TimeUpEvent,
    WinEvent,
)
from src.logical.entities import Player, Ghost
from parser import LevelConfig

logger = logging.getLogger(__name__)


class LogicalMaze:
    """Encapsulate maze generation, movement, and collision rules."""

    def __init__(
        self,
        levels: List[LevelConfig],
        points_pacgum: int = 10,
        points_super_pacgum: int = 50,
        points_ghost: int = 200,
        max_ticks: int = 90 * 60,
        super_pacgum_duration: int = 2500,
        respawn_delay: int = 180,
        invulnerability_duration: int = 120,
        ghost_respawn_delay: int = 300,
    ) -> None:
        """Create a new logical maze with a fresh entity layout.

        Args:
            levels: List of level configurations.
            points_pacgum: Score awarded per normal pellet eaten.
            points_super_pacgum: Score awarded per power pellet eaten.
            points_ghost: Score awarded per ghost eaten while frightened.
            max_ticks: Ticks before TIME_UP fires. Pauses while player is
                in the death countdown so the player is not penalised.
            super_pacgum_duration: Ticks the FRIGHTENED state lasts.
            respawn_delay: Ticks between PLAYER_DIED and auto-respawn.
                The view uses this window to play a death animation.
                PLAYER_RESPAWNED is emitted when the countdown expires.
            invulnerability_duration: Ticks of post-respawn invulnerability.
                Ghost collisions are ignored during this window. The view
                reads player.invulnerability_timer > 0 to show blinking.
            ghost_respawn_delay: Ticks between a ghost being eaten and it
                reappearing at its corner spawn. The view uses
                ghost.respawn_timer > 0 to know which ghosts are waiting.
                GHOST_RESPAWNED is emitted for each ghost that reappears.
        """
        self.levels: List[LevelConfig] = levels
        self.current_level_index: int = 0
        self.current_level = levels[0]
        self.width: int = self.current_level.width
        self.height: int = self.current_level.height
        self.base_seed: int = self.current_level.seed
        self.points_pacgum: int = points_pacgum
        self.points_super_pacgum: int = points_super_pacgum
        self.points_ghost: int = points_ghost
        self.max_ticks: int = max_ticks
        self.elapsed_ticks: int = 0
        self.super_pacgum_duration: int = super_pacgum_duration
        self.respawn_delay: int = respawn_delay
        self.invulnerability_duration: int = invulnerability_duration
        self.ghost_respawn_delay: int = ghost_respawn_delay
        self._death_countdown: int = 0
        self.cheat_invincible: bool = False
        self.cheat_freeze_ghosts: bool = False
        self._pending_events: set[GameEvent] = set()
        self.player: Player = Player(0, 0)
        self.load_level(0)

    def load_level(self, level_idx: int) -> None:
        """Loads a specific level, regenerating the maze and resetting positions."""
        if level_idx < 0 or level_idx >= len(self.levels):
            logger.error(f"Level index {level_idx} out of bounds.")
            return

        self.current_level_idx = level_idx
        self.current_level = self.levels[level_idx]
        self.width = self.current_level.width
        self.height = self.current_level.height
        self.base_seed = self.current_level.seed

        seed = self.base_seed
        self.maze_generator = MazeGenerator((self.width, self.height), seed=seed)
        self.grid = self.maze_generator.maze

        self.elapsed_ticks = 0
        self._death_countdown = 0
        self._pending_events.clear()

        self._spawn_x = self.width // 2 - 1 + (self.width % 2)
        self._spawn_y = self.height // 2

        # Reset Player physical state (KEEP lives and score!)
        self.player.x, self.player.y = self._spawn_x, self._spawn_y
        self.player.state = PlayerState.NORMAL
        self.player.facing = Direction.RIGHT
        self.player.gum_timer = 0
        self.player.invulnerability_timer = 0

        self.ghosts = self._initialize_ghosts()
        self.super_pacgums = self._place_super_pacgums()
        self.pacgums = self._place_pacgums()

    def next_level(self) -> bool:
        """Advances to the next level. Returns False if game is won."""
        if self.current_level_idx + 1 < len(self.levels):
            self.load_level(self.current_level_idx + 1)
            return True
        return False

    def restart_game(self) -> None:
        """Hard reset for a brand new game session."""
        self.player.lives = 3
        self.player.score = 0
        self.load_level(0)

    def _initialize_ghosts(self) -> list[Ghost]:
        """Place ghosts in their four corner spawn points."""
        # 4 corners per PDF specification
        positions = [
            (1, 1),
            (self.width - 2, 1),
            (1, self.height - 2),
            (self.width - 2, self.height - 2),
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
            (self.width - 2, self.height - 2),
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

    @property
    def is_player_invulnerable(self) -> bool:
        """Return True during the post-respawn invulnerability window.

        The view reads this to show a blinking player sprite.
        Ghost collisions are suppressed while this is True.
        """
        return self.player.invulnerability_timer > 0

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
            Direction.LEFT.value: 8,
        }
        if direction_to_wall.get((dx, dy), 0) & self.grid[y1][x1]:
            return False
        return True

    def can_move_direction(
        self, pos: Tuple[int, int], direction: Direction
    ) -> bool:
        """Check whether an entity can move from pos in the given direction."""
        if direction == Direction.NONE:
            return False
        dx, dy = direction.value
        new_pos = (pos[0] + dx, pos[1] + dy)
        return self.can_move(pos, new_pos)

    def can_move_player(self, direction: Direction) -> bool:
        """Check whether the player can move in the given direction."""
        return self.can_move_direction(
            self.player.get_grid_position(), direction
        )

    def _get_valid_moves(
        self, current_pos: Tuple[int, int]
    ) -> List[Direction]:
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

    def _move_ghost(self, ghost: Ghost) -> Direction:
        """Advance a ghost by one step using its current chase behavior.

        Dead ghosts (respawn_timer > 0) are skipped — their respawn is
        handled by tick_timers(), not by movement.
        """
        # Ghost is waiting to respawn — tick_timers handles it
        if ghost.state == GhostState.DEAD:
            return Direction.NONE

        valid_moves = self._get_valid_moves(ghost.get_grid_position())
        if not valid_moves:
            logger.warning(
                "Ghost at %s has no valid moves",
                ghost.get_grid_position(),
            )
            return Direction.NONE

        px, py = self.player.get_grid_position()
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
        else:
            best_dir = max(
                candidates,
                key=lambda d: abs((ghost.x + d.value[0]) - px)
                + abs((ghost.y + d.value[1]) - py),
            )
        return best_dir

    def respawn_player(self) -> None:
        """Reset the player and all ghosts after a death.

        Pellets and score are preserved — only positions and states reset.
        Grants invulnerability_duration ticks of post-respawn protection so
        the player cannot die again the instant they appear.

        Called automatically by tick_timers() when the death countdown
        expires. The view may also call this directly (e.g. from a cheat).
        """
        self.player.x, self.player.y = self._spawn_x, self._spawn_y
        self.player.state = PlayerState.NORMAL
        self.player.facing = Direction.RIGHT
        self.player.gum_timer = 0
        self.player.invulnerability_timer = self.invulnerability_duration
        self._death_countdown = 0

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
            player_invulnerable=self.is_player_invulnerable,
            ghosts=tuple(
                (ghost.x, ghost.y, ghost.state, ghost.ghost_id,
                 ghost.respawn_timer)
                for ghost in self.ghosts
            ),
            pacgums=frozenset(self.pacgums),
            super_pacgums=frozenset(self.super_pacgums),
            ticks_remaining=self.ticks_remaining,
            death_countdown=self._death_countdown,
            is_level_complete=self.is_level_complete,
            is_game_over=self.is_game_over,
            time_up=self.is_time_up,
        )

    def _resolve_item_collisions(self) -> Set[GameEvent]:
        """Check if the player landed on a pellet or power-up."""
        events: Set[GameEvent] = set()
        p_pos = self.player.get_grid_position()
        px, py = p_pos

        if p_pos in self.pacgums:
            self.pacgums.remove(p_pos)
            self.player.score += self.points_pacgum
            events.add(AtePacgumEvent(x=px, y=py,
                                      score_gained=self.points_pacgum))

        elif p_pos in self.super_pacgums:
            self.super_pacgums.remove(p_pos)
            self.player.score += self.points_super_pacgum
            self.player.gum_timer = self.super_pacgum_duration
            self.player.state = PlayerState.POWERED_UP
            events.add(AteSuperPacgumEvent(
                x=px, y=py, score_gained=self.points_super_pacgum))

            for ghost in self.ghosts:
                if ghost.state != GhostState.DEAD:
                    ghost.state = GhostState.FRIGHTENED
                    ghost.last_direction = None

        if self.is_level_complete:
            if self.next_level():
                events.add(LevelCompleteEvent())
            else:
                events.add(WinEvent(final_score=self.player.score))

        return events

    def _resolve_ghost_collision(self, ghost: Ghost) -> Set[GameEvent]:
        """Check if a specific ghost is occupying the same tile as the player.
        Arguments:
            ghost: The ghost to check for collision with the player.
        Returns:
            A set of GameEvents that occurred due to the collision.
        """
        events: Set[GameEvent] = set()

        if ghost.get_grid_position() == self.player.get_grid_position():

            if (ghost.state == GhostState.CHASE
                and not self.cheat_invincible
                    and not self.is_player_invulnerable):

                self.player.lives -= 1
                self.player.state = PlayerState.DEAD

                if self.player.lives <= 0:
                    events.add(GameOverEvent(final_score=self.player.score))
                else:
                    self._death_countdown = self.respawn_delay
                    events.add(PlayerDiedEvent(self.player.lives))

            elif ghost.state == GhostState.FRIGHTENED:
                ghost.state = GhostState.DEAD
                ghost.last_direction = None
                ghost.respawn_timer = self.ghost_respawn_delay
                self.player.score += self.points_ghost

                events.add(AteGhostEvent(
                    ghost_id=ghost.ghost_id,
                    x=ghost.x,
                    y=ghost.y,
                    score_gained=self.points_ghost,
                ))

        return events

    def tick_player(self, player_dir: Direction) -> None:
        """Move the player one step and resolve all collisions.
        Arguments:
            player_dir: The direction the player is attempting to move.
        Returns:
            None
        """
        events: Set[GameEvent] = set()

        if self.player.state == PlayerState.DEAD:
            return

        # 1. Move Player
        if player_dir != Direction.NONE:
            nx = self.player.x + player_dir.value[0]
            ny = self.player.y + player_dir.value[1]
            if self.can_move((self.player.x, self.player.y), (nx, ny)):
                self.player.x, self.player.y = nx, ny
                self.player.facing = player_dir

        # 2. Check Items
        events.update(self._resolve_item_collisions())

        # 3. Check All Ghosts
        for ghost in self.ghosts:
            events.update(self._resolve_ghost_collision(ghost))
            if self.player.state == PlayerState.DEAD:
                break

        self._pending_events.update(events)
        return

    def get_ghost_next_move(self, ghost_id: int) -> Direction:
        """Get the next move for a specific ghost without moving it.
        Arguments:
            ghost_id: The identity of the ghost to query (0–3).
        Returns:
            The Direction the ghost would move next, or Direction.NONE if it
            cannot move.
        """
        ghost = next((g for g in self.ghosts if g.ghost_id == ghost_id), None)
        if not ghost:
            return Direction.NONE

        if ghost.next_move:
            return ghost.next_move

        return Direction.NONE

    def tick_ghost(self, ghost_id: int) -> None:
        """Move a single ghost one step and check if it caught the player.
        Arguments:
            ghost_id: The identity of the ghost to move (0–3).
        Returns:
            None
        """
        events: Set[GameEvent] = set()

        if self.player.state == PlayerState.DEAD or self.cheat_freeze_ghosts:
            return

        # Locate the specific ghost
        ghost = next((g for g in self.ghosts if g.ghost_id == ghost_id), None)
        if not ghost:
            return

        # 1. Move the Ghost
        if ghost.next_move:
            # If a next_move is queued, move in that direction
            nx = ghost.x + ghost.next_move.value[0]
            ny = ghost.y + ghost.next_move.value[1]
            ghost.x, ghost.y = nx, ny
            ghost.last_direction = ghost.next_move
        else:
            # Otherwise, determine the next move
            best_dir = self._move_ghost(ghost)
            if best_dir != Direction.NONE:
                nx = ghost.x + best_dir.value[0]
                ny = ghost.y + best_dir.value[1]
                ghost.x, ghost.y = nx, ny
                ghost.last_direction = best_dir

        # Queue the next move for the ghost
        ghost.next_move = self._move_ghost(ghost)


        # 2. Check Collision with Player ONLY
        events.update(self._resolve_ghost_collision(ghost))

        self._pending_events.update(events)
        return

    def tick_timers(self) -> None:
        """Advance all time-based state by one frame.

        Call this every frame regardless of player/ghost speed.
        Handles five independent countdowns:

        - Player death countdown: counts down after PlayerDiedEvent, then
        auto-respawns the player and emits PlayerRespawnedEvent. The level
        timer is paused during this window.
        - Player invulnerability: counts down after a respawn. Ghost
        collisions are suppressed while it is active.
        - Ghost respawn countdowns: one per dead ghost. When each expires,
        that specific ghost teleports to its corner and emits
        GhostRespawnedEvent(ghost_id, x, y) so the view knows exactly
        which ghost reappeared and where.
        - Power-up countdown: emits PowerUpExpiredEvent when it runs out
        and returns all FRIGHTENED ghosts to CHASE.
        - Level clock: advances elapsed_ticks and emits TimeUpEvent when
        the time limit is reached.

        Returns:
            None
        """
        events: Set[GameEvent] = set()

        # 1. Player death countdown
        if self._death_countdown > 0:
            self._death_countdown -= 1
            if self._death_countdown == 0:
                self.respawn_player()
                events.add(PlayerRespawnedEvent(
                    x=self._spawn_x,
                    y=self._spawn_y,
                ))
            self._pending_events.update(events)
            return  # level timer pauses during death countdown

        # 2. Player invulnerability countdown
        if self.player.invulnerability_timer > 0:
            self.player.invulnerability_timer -= 1

        # 3. Ghost respawn countdowns
        for ghost in self.ghosts:
            if ghost.state == GhostState.DEAD and ghost.respawn_timer > 0:
                ghost.respawn_timer -= 1
                if ghost.respawn_timer == 0:
                    gx, gy = ghost.spawn_point
                    ghost.x, ghost.y = gx, gy
                    # Respawn as FRIGHTENED if power-up is still active
                    ghost.state = (
                        GhostState.FRIGHTENED
                        if self.player.state == PlayerState.POWERED_UP
                        else GhostState.CHASE
                    )
                    ghost.last_direction = None
                    events.add(GhostRespawnedEvent(
                        ghost_id=ghost.ghost_id,
                        x=gx,
                        y=gy,
                    ))

        # 4. Power-up countdown
        if self.player.gum_timer > 0:
            self.player.gum_timer -= 1
            if self.player.gum_timer <= 0:
                self.player.state = PlayerState.NORMAL
                for ghost in self.ghosts:
                    if ghost.state == GhostState.FRIGHTENED:
                        ghost.state = GhostState.CHASE
                events.add(PowerUpExpiredEvent())

        # 5. Level clock
        self.elapsed_ticks += 1
        if self.is_time_up:
            events.add(TimeUpEvent())

        self._pending_events.update(events)
        return

    def flush_events(self) -> set[GameEvent]:
        """Returns all queued events and clears the internal queue."""
        events_to_return = self._pending_events.copy()
        self._pending_events.clear()
        return events_to_return
