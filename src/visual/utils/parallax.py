from src.visual import Node, Context
from typing import List, Tuple
from pygame import Vector2, Surface


class ParallaxLayer(Node):
    def __init__(self, context: Context, surface: Surface, velocity: float, speed: float) -> None:
        super().__init__(context)
        self.surface = surface
        self.velocity = velocity * speed

    def _on_update(self, delta: float) -> None:
        self.local_position.x += self.velocity * delta
        while self.local_position.x > self.surface.get_width():
            self.local_position.x -= self.surface.get_width()

    def _on_draw(self):
        self.context.screen.blit(self.surface, self.local_position)
        self.context.screen.blit(self.surface, self.local_position - Vector2(self.surface.get_width(), 0))


class Parallax(Node):
    def __init__(self, context: Context, layers: List[Tuple[Surface, float]], velocity: float) -> None:
        super().__init__(context)
        self.layers = layers
        self.velocity = velocity
        self._create_layers()

    def _create_layers(self) -> None:
        for surface, speed in self.layers:
            layer = ParallaxLayer(self.context, surface, self.velocity, speed)
            self.add_child(layer)
