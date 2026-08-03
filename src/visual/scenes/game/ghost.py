"""A module for the visual representation of ghosts in the game."""

from src.logical.core_types import GhostState
from src.visual.utils.particle import ParticleSystem
import pygame
from src.logical.entities import Ghost
from src.logical.maze import LogicalMaze
from src.visual import Node, Context
from src.visual.utils.sprite import Sprite
from pygame import Surface, Color, Vector2


class VisualGhost(Node):
    """A class representing the visual representation of a ghost in the game.

    Attributes:
        id (int): The unique identifier for the ghost.
        logical_maze (LogicalMaze): The logical representation of the maze.
        logical_ghost (Ghost): The logical representation of the ghost.
        step_size (int): The size of each step the ghost takes in the maze.
        target_position (Vector2): Target position of the ghost in the maze.
        animated_position (Vector2): Current animated position of the ghost.
        ghost_step_timer (float): Timer to track the duration of ghost step.
        speed (float): The speed at which the ghost moves.
        ghost_step_duration (float): The duration of each ghost step.
        sprite_neutral (Sprite): The sprite for the ghost in its neutral state.
        sprite_running (Sprite): The sprite for the ghost in its running state.
        particles (ParticleSystem): The particle system for the ghost.

    """

    def __init__(
        self,
        context: Context,
        id: int,
        maze: LogicalMaze,
        ghost: Ghost,
        step_size: int,
        speed: float,
    ) -> None:
        """Initialize the VisualGhost object."""
        super().__init__(context)
        self.id = id
        self.logical_maze = maze
        self.logical_ghost = ghost
        self.step_size = step_size
        self.target_position = Vector2(ghost.x, ghost.y) * step_size
        self.animated_position = self.target_position.copy()

        self.ghost_step_timer = 0
        self.speed = speed
        self.ghost_step_duration = step_size / self.speed

        self.sprite_neutral = Sprite(
            context,
            context.assets.image("ghost_neutral"),
            1,
            2,
            5,
            True,
        )
        self.sprite_running = Sprite(
            context,
            context.assets.image("ghost_running"),
            1,
            4,
            17,
            True,
        )
        particle_img = Surface((1, 1), flags=pygame.SRCALPHA)
        particle_color = Color("white")
        particle_color.a = 100
        particle_img.fill(particle_color)
        self.particles = ParticleSystem(
            context,
            particle_img,
            (Vector2(10, 10), Vector2(-10, -10)),
            (Vector2(0, 0), Vector2(0, 0)),
            0.4,
            20,
        )

    def _on_update(self, delta: float) -> None:
        """Update the visual representation of the ghost.

        Args:
            delta (float): The time elapsed since the last update.

        """
        match self.logical_ghost.state:
            case GhostState.FRIGHTENED:
                current_sprite = self.sprite_running
                self.particles.update(delta)
            case _:
                current_sprite = self.sprite_neutral
        current_sprite.update(delta)
        current_sprite.flip_x = (
            self.animated_position.x < self.target_position.x
        )
        self.particles.local_position = (
            self.world_position + self.animated_position
        )
        self.ghost_step_timer += delta
        if self.ghost_step_timer > self.ghost_step_duration:
            self.logical_maze.tick_ghost(self.id)
            self.ghost_step_timer = 0

        self.target_position = (
            Vector2(self.logical_ghost.x, self.logical_ghost.y)
            * self.step_size
        )
        self.animated_position = self.animated_position.move_towards(
            self.target_position, self.speed * delta
        )

    def _on_draw(self) -> None:
        """Draw the visual representation of the ghost."""
        match self.logical_ghost.state:
            case GhostState.FRIGHTENED:
                current_sprite = self.sprite_running
                self.particles.render()
            case _:
                current_sprite = self.sprite_neutral
        current_sprite.local_position = (
            self.world_position + self.animated_position
        )
        current_sprite.render()

    def respawn(self, x, y):
        """Respawn the ghost at the specified coordinates.

        Args:
            x (int): The x-coordinate to respawn the ghost.
            y (int): The y-coordinate to respawn the ghost.

        """
        self.target_position = Vector2(x, y) * self.step_size
        self.animated_position = self.target_position.copy()
        self.dead = False

    def _on_redraw(self) -> None:
        """Redraw the ghost's sprites."""
        self.sprite_neutral.redraw()
        self.sprite_running.redraw()
