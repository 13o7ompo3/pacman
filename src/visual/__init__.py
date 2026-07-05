from abc import ABC, abstractmethod

from pygame import Surface
from pygame.event import Event


class GameComponent(ABC):
    @abstractmethod
    def update(self, delta: float) -> None:
        """Update a component state."""
        ...

    def handle_event(self, event: Event) -> None:
        """Handle an input event."""
        ...


class DrawableComponent(GameComponent):
    @abstractmethod
    def render(self, scree: Surface) -> None:
        """Handle drawing the visuals of a component."""
        ...
