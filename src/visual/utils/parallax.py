"""This module provides utility classes for implementing parallax
scrolling effects in Pygame."""

from src.visual import Node, Context
from typing import List, Tuple
from pygame import Vector2, Surface


class ParallaxLayer(Node):
    """A class representing a single layer in a parallax scrolling effect."""

    def __init__(
        self, context: Context, surface: Surface, velocity: float, speed: float
    ) -> None:
        """Initialize a ParallaxLayer instance.

        Args:
            context (Context): The context in which the layer exists.
            surface (Surface): The surface representing the layer's image.
            velocity (float): The base velocity of the layer.
            speed (float): The speed multiplier for the layer's movement.
        """
        super().__init__(context)
        self.surface = surface
        self.velocity = velocity * speed

    def _on_update(self, delta: float) -> None:
        """Update the position of the layer based on the elapsed time.

        Args:
            delta (float): The time elapsed since the last update, in seconds.
        """
        self.local_position.x += self.velocity * delta
        while self.local_position.x > self.surface.get_width():
            self.local_position.x -= self.surface.get_width()

    def _on_draw(self):
        """Draw the layer on the screen,
        handling wrapping for continuous scrolling.
        """
        self.context.screen.blit(self.surface, self.local_position)
        self.context.screen.blit(
            self.surface,
            self.local_position - Vector2(self.surface.get_width(), 0),
        )


class Parallax(Node):
    """A class representing a parallax scrolling effect with multiple layers."""

    def __init__(
        self,
        context: Context,
        layers: List[Tuple[Surface, float]],
        velocity: float,
    ) -> None:
        """Initialize a Parallax instance.

        Args:
            context (Context): The context in which the parallax effect exists.
            layers (List[Tuple[Surface, float]]): A list of tuples, each
                containinga surface and its corresponding speed multiplier.
            velocity (float): The base velocity for the parallax effect.
        """
        super().__init__(context)
        self.layers = layers
        self._velocity = velocity
        self._create_layers()

    @property
    def velocity(self) -> float:
        """Get the curren velocity.

        Returns:
            float: the velocity.

        """
        return self._velocity

    @velocity.setter
    def velocity(self, value: float) -> None:
        """Set a new velocity value for all layers.

        Args:
            value (float): the new value.

        """
        for layer in self.children:
            if isinstance(layer, ParallaxLayer):
                layer.velocity /= self._velocity
                layer.velocity *= value
        self._velocity = value

    def _create_layers(self) -> None:
        """Create and add ParallaxLayer instances
        for each layer in the parallax effect.
        """
        for surface, speed in self.layers:
            layer = ParallaxLayer(self.context, surface, self._velocity, speed)
            self.add_child(layer)
