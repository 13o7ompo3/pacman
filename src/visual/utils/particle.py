"""This module provides utility classes
for implementing particle systems in Pygame."""

import random

from pygame import Surface

from src.visual import Context, Node
from src.visual.utils.sprite import Sprite
from src.visual.utils.primitives import Vec2


class Particle(Node):
    """A class representing a single particle in a particle system."""

    def __init__(
        self,
        context: Context,
        particle_object: Surface | Sprite,
        position: Vec2,
        velocity: Vec2,
        acceleration: Vec2,
        lifetime: float,
    ) -> None:
        """Initialize a Particle instance.

        Args:
            context (Context): The context in which the particle exists.
            particle_object (Surface | Sprite): The image of one particle.
            position (Vec2): The initial position of the particle.
            velocity (Vec2): The initial velocity of the particle.
            acceleration (Vec2): The acceleration of the particle.
            lifetime (float): The lifetime of the particle, in seconds.
        """
        super().__init__(context)
        if isinstance(particle_object, Sprite):
            self.particle_object: Sprite | Surface = Sprite(
                context,
                particle_object.surface,
                particle_object.rows,
                particle_object.cols,
                particle_object.fps,
                particle_object.repeat,
            )
        else:
            self.particle_object = particle_object
        self.local_position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.lifetime = lifetime
        self.age = 0.0

    def _on_update(self, delta: float) -> None:
        """Update the particle's position and age.

        Args:
            delta (float): The time elapsed since the last update,
              in seconds.
        """
        self.age += delta
        if self.age >= self.lifetime:
            self.free_from_scene()
            return

        self.local_position += self.velocity * delta
        self.velocity += self.acceleration * delta
        if isinstance(self.particle_object, Sprite):
            self.particle_object.local_position = self.local_position
            self.particle_object.update(delta)
            if not self.particle_object.playing:
                self.free_from_scene()

    def _on_draw(self) -> None:
        """Draw the particle on the screen if it is still alive."""
        if isinstance(self.particle_object, Sprite):
            self.particle_object.render()
        else:
            self.context.screen.blit(
                self.particle_object, tuple(self.local_position.array)
            )


class ParticleSystem(Node):
    """A class representing a particle system that emits particles."""

    def __init__(
        self,
        context: Context,
        particle_object: Surface | Sprite,
        velocity_range: tuple[Vec2, Vec2],
        acceleration_range: tuple[Vec2, Vec2],
        lifetime: float,
        amount: int,
    ) -> None:
        """Initialize a ParticleSystem instance.

        Args:
            context (Context): The context in which the particle system exists.
            surface (Surface): The surface representing the particles' image.
            velocity_range (Tuple[Vec2, Vec2]): A tuple containing the
                minimum and maximum velocity vectors for emitted particles.
            acceleration_range (Tuple[Vec2, Vec2]): A tuple containing
                the minimum and maximum acceleration vectors
                for emitted particles.
            lifetime (float): The lifetime of each particle, in seconds.
            amount (int): The number of existing particles at any given time.
        """
        super().__init__(context)
        self.particle_object = particle_object
        self.velocity_range = velocity_range
        self.acceleration_range = acceleration_range
        self.lifetime = lifetime
        self.amount = amount
        self.emission_rate = self.amount / self.lifetime
        self.time_since_last_emission = 0.0
        self.playing = True

    def _on_update(self, delta: float) -> None:
        """Update the particle system and emit new particles as needed.

        Args:
            delta (float): The time elapsed since the last update.
        """
        if not self.playing:
            return
        self.time_since_last_emission += delta
        while self.time_since_last_emission >= 1.0 / self.emission_rate:
            self.time_since_last_emission -= 1.0 / self.emission_rate
            velocity = Vec2(
                random.uniform(
                    self.velocity_range[0].x, self.velocity_range[1].x
                ),
                random.uniform(
                    self.velocity_range[0].y, self.velocity_range[1].y
                ),
            )
            acceleration = Vec2(
                random.uniform(
                    self.acceleration_range[0].x, self.acceleration_range[1].x
                ),
                random.uniform(
                    self.acceleration_range[0].y, self.acceleration_range[1].y
                ),
            )
            new_particle = Particle(
                context=self.context,
                particle_object=self.particle_object,
                position=self.world_position.copy(),
                velocity=velocity,
                acceleration=acceleration,
                lifetime=self.lifetime,
            )
            self.add_child(new_particle)

    def play(self) -> None:
        """Start emitting particles."""
        self.playing = True

    def stop(self) -> None:
        """Stop emitting particles."""
        self.playing = False
