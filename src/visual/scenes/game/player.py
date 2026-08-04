"""A module containing the Player class for the game."""

import pygame
from pygame import KEYDOWN, Color, Surface, Vector2
from pygame.event import Event

from src.logical.maze import Direction, LogicalMaze
from src.visual import Context, Node
from src.visual.utils.particle import ParticleSystem
from src.visual.utils.sprite import Sprite


class Player(Node):
    """A class representing the player in the game.

    Attributes:
        direction (Direction): The current direction of the player.
        next_direction (Direction): The next direction the player will move in.
        target_position (Vector2): Target position of the player in the maze.
        animated_position (Vector2): Current animated position of the player.
        step_size (int): The size of each step the player takes in the maze.
        maze (LogicalMaze): The logical representation of the maze.
        speed (float): The speed at which the player moves.
        dead (bool): Whether the player is dead or not.
        sprites (dict): A dictionary of sprites for each direction.
        idle_img (Surface): The image to display when the player is idle.
        particle_img (Surface): The image to use for the particle system.
        particles (ParticleSystem): The particle system for the player.

    """

    def __init__(
        self,
        context: Context,
        maze: LogicalMaze,
        step_size: int,
        speed: float = 80,
    ) -> None:
        """Initialize the Player object."""
        super().__init__(context)
        self.direction = None
        self.next_direction = None
        self.target_position = (
            Vector2(maze.player.x, maze.player.y) * step_size
        )
        self.animated_position = self.target_position.copy()
        self.step_size = step_size
        self.maze = maze
        self.speed = speed
        self.dead = False
        self.sprites = {
            Direction.UP: Sprite(
                context,
                self.context.assets.image("player_up"),
                1,
                4,
                10,
                True,
            ),
            Direction.DOWN: Sprite(
                context,
                self.context.assets.image("player_down"),
                1,
                4,
                10,
                True,
            ),
            Direction.LEFT: Sprite(
                context,
                self.context.assets.image("player_left"),
                1,
                4,
                10,
                True,
            ),
            Direction.RIGHT: Sprite(
                context,
                self.context.assets.image("player_right"),
                1,
                4,
                10,
                True,
            ),
        }
        self.idle_img = self.context.assets.image("player_idle")
        self.particle_img = Surface(
            (2, 2), flags=pygame.SRCALPHA
        ).convert_alpha()
        particle_color = Color(self.context.colors.lightest)
        particle_color.a = 100
        self.particle_img.fill(particle_color)
        self.particles = ParticleSystem(
            context,
            self.particle_img,
            (Vector2(10, 10), Vector2(-10, -10)),
            (Vector2(0, 0), Vector2(0, 0)),
            0.4,
            20,
        )

    def _on_input(self, event: Event) -> Event | None:
        """Handle input events for the player."""
        if self.hidden:
            return
        if event.type == KEYDOWN:
            if event.key in {pygame.K_UP, pygame.K_w, pygame.K_k}:
                self.next_direction = Direction.UP
            if event.key in {pygame.K_DOWN, pygame.K_s, pygame.K_j}:
                self.next_direction = Direction.DOWN
            if event.key in {pygame.K_LEFT, pygame.K_a, pygame.K_h}:
                self.next_direction = Direction.LEFT
            if event.key in {pygame.K_RIGHT, pygame.K_d, pygame.K_l}:
                self.next_direction = Direction.RIGHT
            if self.direction is None and self.next_direction is not None:
                self.direction = self.next_direction
                player_pos = self.maze.player.get_grid_position()
                if self.maze.can_move(
                    player_pos,
                    (
                        player_pos[0] + self.direction.value[0],
                        player_pos[1] + self.direction.value[1],
                    ),
                ):
                    self.target_position = (
                        Vector2(player_pos) + self.direction.value
                    ) * self.step_size
        return event

    def _on_update(self, delta: float) -> None:
        """Update the player's state."""
        self.particles.update(delta)
        if not self.dead:
            self.animated_position = self.animated_position.move_towards(
                self.target_position, delta * self.speed
            )
            self.particles.local_position = (
                self.world_position + self.animated_position
            )

        if self.animated_position == self.target_position:
            self._step_target_position()
        elif self.direction is not None:
            self.sprites[self.direction].update(delta)

    def _step_target_position(self):
        """Update the target position of the player based the direction."""
        if self.direction is not None:
            self.maze.tick_player(self.direction)
            player_pos = self.maze.player.get_grid_position()
            if self.next_direction and self.maze.can_move_player(
                self.next_direction
            ):
                self.direction = self.next_direction
            if self.maze.can_move(
                player_pos,
                (
                    player_pos[0] + self.direction.value[0],
                    player_pos[1] + self.direction.value[1],
                ),
            ):
                self.target_position = (
                    Vector2(player_pos) + self.direction.value
                ) * self.step_size

    def respawn(self, x, y):
        """Respawn the player at the given grid coordinates (x, y)."""
        self.target_position = Vector2(x, y) * self.step_size
        self.animated_position = self.target_position.copy()

    def _on_draw(self) -> None:
        """Draw the player and its particles on the screen."""
        self.particles.render()
        if self.direction is not None:
            sprite = self.sprites[self.direction]
            sprite.local_position = (
                self.world_position + self.animated_position
            )
            sprite.render()
        else:
            self.context.screen.blit(
                self.idle_img,
                self.world_position
                + self.animated_position
                - Vector2(self.idle_img.get_size()) / 2,
            )

    def _on_redraw(self) -> None:
        """Redraw the player and its particles."""
        particle_color = Color(self.context.colors.lightest)
        particle_color.a = 100
        self.particle_img.fill(particle_color)
        for sprite in self.sprites.values():
            sprite.redraw()
