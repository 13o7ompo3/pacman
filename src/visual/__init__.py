from abc import ABC, abstractmethod

from pygame import Surface, Vector2
from pygame.event import Event
from typing import final


class GameComponent(ABC):
    def __init__(self) -> None:
        self.parent: "GameComponent | None" = None
        self.children: "list[GameComponent]" = []

    @final
    def update(self, delta: float) -> None:
        """Update a component's state and its children."""
        self._on_update(delta)
        for child in self.children:
            child.update(delta)

    @abstractmethod
    def _on_update(self, delta: float) -> None:
        """Inhirit to update component"""
        ...

    @final
    def handle_input(self, event: Event) -> None:
        """Handle an input event for current and all children."""
        self._on_input(event)
        for child in self.children:
            child.handle_input(event)

    def _on_input(self, event: Event) -> None:
        """Handle input for component"""
        ...

    @final
    def add_child(self, child: "GameComponent") -> None:
        """Add a child component to this one."""
        self.children.append(child)
        child.parent = self

    @final
    def remove_child(self, child: "GameComponent") -> None:
        """Remove a child component to this one."""
        self.children.remove(child)
        child.parent = None


class Node(GameComponent):
    def __init__(self) -> None:
        super().__init__()
        self.local_position: Vector2 = Vector2()

    @property
    def world_position(self) -> Vector2:
        """Get the absolute world position calculated from relative parent positions"""
        if isinstance(self.parent, Node):
            return self.parent.world_position + self.local_position
        else:
            return self.local_position

    @final
    def render(self, screen: Surface) -> None:
        """Handle drawing the visuals of a component and it's children."""
        self._on_draw(screen)

        for child in self.children:
            if isinstance(child, Node):
                child.render(screen)

    def _on_draw(self, screen: Surface) -> None:
        """Override to draw component."""
        ...
