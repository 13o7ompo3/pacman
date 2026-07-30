from src.visual import Node, Context
from pygame import Surface, Vector2
import random
from typing import Dict, Tuple
from src.visual.utils.image import Image

class Particle(Node):
    def __init__(
        self,
        context: Context,
        surface: Surface,
        position: Vector2,
        velocity: Vector2,
        acceleration: Vector2,
        lifetime: float,
    ) -> None:
        super().__init__(context)
        self.surface = surface
        self.local_position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.lifetime = lifetime
        self.age = 0.0

    def _on_update(self, delta_time: float) -> None:
        self.age += delta_time
        if self.age >= self.lifetime:
            self.free_from_scene()
            return

        self.local_position += self.velocity * delta_time
        self.velocity += self.acceleration * delta_time

    def _on_draw(self) -> None:
        if self.age < self.lifetime:
            self.context.screen.blit(self.surface, tuple(map(int, self.local_position)))

class ParticleSystem(Node):
    def __init__(
        self,
        context: Context,
        surface: Surface,
        velocity_range: Tuple[Vector2, Vector2],
        acceleration_range: Tuple[Vector2, Vector2],
        lifetime: float,
        amount: int,
    ) -> None:
        super().__init__(context)
        self.surface = surface
        self.velocity_range = velocity_range
        self.acceleration_range = acceleration_range
        self.lifetime = lifetime
        self.amount = amount
        self.emission_rate = self.amount / self.lifetime
        self.time_since_last_emission = 0.0

    def _on_update(self, delta_time: float) -> None:
        self.time_since_last_emission += delta_time
        while self.time_since_last_emission >= 1.0 / self.emission_rate:
            self.time_since_last_emission -= 1.0 / self.emission_rate
            velocity = Vector2(
                random.uniform(self.velocity_range[0].x, self.velocity_range[1].x),
                random.uniform(self.velocity_range[0].y, self.velocity_range[1].y),
            )
            acceleration = Vector2(
                random.uniform(self.acceleration_range[0].x, self.acceleration_range[1].x),
                random.uniform(self.acceleration_range[0].y, self.acceleration_range[1].y),
            )
            new_particle = Particle(
                context=self.context,
                surface=self.surface,
                position=self.world_position.copy(),
                velocity=velocity,
                acceleration=acceleration,
                lifetime=self.lifetime,
            )
            self.add_child(new_particle)

    def _on_draw(self) -> None:
        pass
