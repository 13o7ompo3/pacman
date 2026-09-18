"""A module containing the Player class for the game."""

import pygame
from pygame import KEYDOWN, Color, PixelArray, Surface
from pygame.event import Event

from src.logical.maze import Direction, LogicalMaze
from src.visual import Context, Node
from src.visual.utils.particle import ParticleSystem
from src.visual.utils.sprite import Sprite
from src.visual.utils.timer import Timer
from src.visual.utils.primitives import Vec2


class Player(Node):
    """A class representing the player in the game.

    Attributes:
        direction (Direction): The current direction of the player.
        next_direction (Direction): The next direction the player will move in.
        target_position (Vec2): Target position of the player in the maze.
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
        """Initialize the Player object.

        Args:
            context (Context): The context in which the player exists.
            maze (LogicalMaze): The logical representation of the maze.
            step_size (int): The size of each step.
            speed (float): The speed at which the player moves.
        """
        super().__init__(context)
        self.direction: Direction | None = None
        self.next_direction: Direction | None = None
        self.target_position = (
            Vec2(maze.player.x, maze.player.y) * step_size
            + Vec2(step_size, step_size) / 2
        )
        self.local_position = self.target_position.copy()
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
        self.idle_img = context.assets.image("player_idle")
        particle_img = context.assets.image("particle_2x2")
        self._set_surface_alpha(particle_img, 100)
        particle_scatter = 12
        self.particles = ParticleSystem(
            context,
            particle_img,
            (
                Vec2(particle_scatter, particle_scatter),
                Vec2(-particle_scatter, -particle_scatter),
            ),
            (Vec2(0, 0), Vec2(0, 0)),
            0.4,
            20,
        )
        particle_img = context.assets.image("particle_4x4")
        particle_scatter = 100
        death_particles = ParticleSystem(
            context,
            particle_img,
            (
                Vec2(particle_scatter, particle_scatter),
                Vec2(-particle_scatter, -particle_scatter),
            ),
            (Vec2(0, 0), Vec2(0, 0)),
            0.2,
            20,
        )
        death_particles.playing = False

        def on_death_particles_timer_start(timer: Timer) -> None:
            """Start the death particles when the timer starts.

            Args:
                timer (Timer): The timer that started.
            """
            death_particles.play()

        def on_death_particles_timer_finished(timer: Timer) -> None:
            """Stop the particles and hide the player when the timer finishes.

            Args:
                timer (Timer): The timer that finished.
            """
            death_particles.stop()
            self.hidden = True

        self.death_particles_timer = Timer(
            0.4,
            on_start=on_death_particles_timer_start,
            on_finish=on_death_particles_timer_finished,
        )
        self.add_child(death_particles)
        self.add_child(self.death_particles_timer)
        self.super_pacgum_silhouette = ParticleSystem(
            context,
            Sprite(
                context,
                context.assets.image("player_silhouette"),
                1,
                4,
                10,
                False,
            ),
            (Vec2(), Vec2()),
            (Vec2(), Vec2()),
            0.4,
            4,
        )

    def _set_surface_alpha(self, surface: Surface, alpha: int) -> None:
        """Set the alpha value of a Pygame Surface.

        Args:
            surface (Surface): The Pygame Surface to modify.
            alpha (int): The alpha value to set (0-255).

        """
        with PixelArray(surface) as array:
            w, h = surface.get_size()
            for x in range(w):
                for y in range(h):
                    color = Color(array[x, y])  # type: ignore[index]
                    color.a = alpha
                    array[x, y] = color  # type: ignore[index]

    def _on_input(self, event: Event) -> Event | None:
        """Handle input events for the player.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event if it was not handled, otherwise None.

        """
        if self.hidden:
            return None
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
                if self.direction and self.maze.can_move(
                    player_pos,
                    (
                        player_pos[0] + self.direction.value[0],
                        player_pos[1] + self.direction.value[1],
                    ),
                ):
                    self.target_position = (
                        Vec2(player_pos) + self.direction.value
                    ) * self.step_size + Vec2(
                        self.step_size, self.step_size
                    ) / 2
        return event

    def _on_update(self, delta: float) -> None:
        """Update the player's state.

        Args:
            delta (float): The time elapsed since the last update.

        """
        self.particles.update(delta)
        self.super_pacgum_silhouette.update(delta)
        if not self.dead:
            self.local_position = self.local_position.move_towards(
                self.target_position, delta * self.speed
            )
            self.particles.local_position = self.world_position
            self.super_pacgum_silhouette.local_position = self.world_position

        if self.local_position == self.target_position:
            self._step_target_position()
        elif self.direction is not None:
            self.sprites[self.direction].update(delta)

    def _step_target_position(self) -> None:
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
                    Vec2(player_pos) + self.direction.value
                ) * self.step_size + Vec2(self.step_size) / 2

    def die(self) -> None:
        """Handle the player's death."""
        self.dead = True
        self.death_particles_timer.start()
        self.direction = None
        self.next_direction = None

    def respawn(self, x: int, y: int) -> None:
        """Respawn the player at the given grid coordinates (x, y).

        Args:
            x (int): The x-coordinate to respawn the player.
            y (int): The y-coordinate to respawn the player.

        """
        self.dead = False
        self.hidden = False
        self.target_position = (
            Vec2(x, y) * self.step_size
            + Vec2(self.step_size, self.step_size) / 2
        )
        self.local_position = self.target_position.copy()

    def _on_draw(self) -> None:
        """Draw the player and its particles on the screen."""
        self.super_pacgum_silhouette.render()
        if self.local_position != self.target_position:
            if self.maze.player.gum_timer > 0:
                self.super_pacgum_silhouette.play()
                self.particles.stop()
            else:
                self.particles.play()
                self.super_pacgum_silhouette.stop()
        else:
            self.particles.stop()
            self.super_pacgum_silhouette.stop()
        self.particles.render()
        if self.direction is not None:
            sprite = self.sprites[self.direction]
            sprite.local_position = self.world_position
            sprite.render()
        else:
            self.context.screen.blit(
                self.idle_img,
                self.world_position - Vec2(self.idle_img.get_size()) / 2,
            )

    def _on_redraw(self) -> None:
        """Redraw the player and its particles."""
        for sprite in self.sprites.values():
            sprite.redraw()
