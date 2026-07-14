from abc import ABC, abstractmethod

from pygame import Surface, Vector2
from pygame.event import Event
from typing import final

from pygame.font import Font


class GameComponent(ABC):
    def __init__(self) -> None:
        self.parent: "GameComponent | None" = None
        self.children: "list[GameComponent]" = []
        self.paused = False

    @final
    def update(self, delta: float) -> None:
        """Update a component's state and its children."""
        if self.paused:
            return

        self._on_update(delta)
        for child in self.children:
            child.update(delta)

    def _on_update(self, delta: float) -> None:
        """Inherit to update component"""
        ...

    @final
    def handle_input(self, event: Event) -> None | Event:
        """Handle an input event for current and all children."""
        propagate_event = True

        for child in self.children[::-1]:
            ret = child.handle_input(event)
            if ret is None:
                return

        if propagate_event:
            return self._on_input(event)

    def _on_input(self, event: Event) -> Event | None:
        """Handle input for component optionally returning it to be passed to it's parent"""
        return event

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

    @final
    def clear_children(self) -> None:
        """Remove a child component to this one."""
        self.children.clear()


class Node(GameComponent):
    def __init__(self, context: "Context") -> None:
        super().__init__()
        self.local_position: Vector2 = Vector2()
        self.context = context
        self.hidden = False

    @property
    def world_position(self) -> Vector2:
        """Get the absolute world position calculated from relative parent positions"""
        if isinstance(self.parent, Node):
            return self.parent.world_position + self.local_position
        else:
            return self.local_position

    @final
    def render(self) -> None:
        """Handle drawing the visuals of a component and it's children."""
        if self.hidden:
            return

        self._on_draw()

        for child in self.children:
            if isinstance(child, Node):
                child.render()

    def _on_draw(self) -> None:
        """Override to draw component."""
        ...


class Context:
    def __init__(
        self,
        screen: Surface,
        width: int,
        height: int,
        font: Font,
    ) -> None:
        self.root_scene = Node(self)
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.game_running = True
