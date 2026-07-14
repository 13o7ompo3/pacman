from dataclasses import dataclass

__all__ = [
    "GameEvent",
    "AtePacgumEvent",
    "AteSuperPacgumEvent",
    "AteGhostEvent",
    "PlayerDiedEvent",
    "PlayerRespawnedEvent",
    "GhostRespawnedEvent",
    "PowerUpExpiredEvent",
    "LevelCompleteEvent",
    "GameOverEvent",
    "TimeUpEvent",
]


@dataclass(frozen=True)
class GameEvent:
    """Base class for all events emitted by the logical layer."""


@dataclass(frozen=True)
class AtePacgumEvent(GameEvent):
    """Player collected a normal pellet.

    Attributes:
        x: Column of the eaten pellet.
        y: Row of the eaten pellet.
        score_gained: Points added this event.
    """
    x: int
    y: int
    score_gained: int


@dataclass(frozen=True)
class AteSuperPacgumEvent(GameEvent):
    """Player collected a power pellet — all non-dead ghosts now FRIGHTENED.

    Attributes:
        x: Column of the eaten pellet.
        y: Row of the eaten pellet.
        score_gained: Points added this event.
    """
    x: int
    y: int
    score_gained: int


@dataclass(frozen=True)
class AteGhostEvent(GameEvent):
    """Player ate a FRIGHTENED ghost.

    Attributes:
        ghost_id: Identity of the eaten ghost (0–3).
        x: Column where the ghost was eaten.
        y: Row where the ghost was eaten.
        score_gained: Points added this event.
    """
    ghost_id: int
    x: int
    y: int
    score_gained: int


@dataclass(frozen=True)
class PlayerDiedEvent(GameEvent):
    """Player touched a CHASE ghost and lost one life.

    lives_remaining > 0: respawn countdown is running.
    Use PlayerRespawnedEvent to know when the player is back.

    Attributes:
        lives_remaining: Lives left after this death (always > 0 here;
            use GameOverEvent when lives reach zero).
    """
    lives_remaining: int


@dataclass(frozen=True)
class PlayerRespawnedEvent(GameEvent):
    """Player respawned after the death countdown expired.

    Attributes:
        x: Column of the respawn position.
        y: Row of the respawn position.
    """
    x: int
    y: int


@dataclass(frozen=True)
class GhostRespawnedEvent(GameEvent):
    """One specific ghost finished its respawn countdown and is active again.

    Attributes:
        ghost_id: Identity of the respawned ghost (0–3).
        x: Column of the ghost's spawn corner.
        y: Row of the ghost's spawn corner.
    """
    ghost_id: int
    x: int
    y: int


@dataclass(frozen=True)
class PowerUpExpiredEvent(GameEvent):
    """The FRIGHTENED power-up timer ran out — all FRIGHTENED ghosts
    reverted to CHASE."""


@dataclass(frozen=True)
class LevelCompleteEvent(GameEvent):
    """All pellets and power pellets have been eaten."""


@dataclass(frozen=True)
class GameOverEvent(GameEvent):
    """Player lost all lives — game has ended.

    Attributes:
        final_score: Total score at the moment of game over.
    """
    final_score: int


@dataclass(frozen=True)
class TimeUpEvent(GameEvent):
    """Level time limit reached."""
