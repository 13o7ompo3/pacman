"""A module that defines the base classes for game components and nodes."""

from typing import final

from pygame import Surface, Vector2
from pygame.event import Event

from parser import Config
from src.db_manager.user import UserManager
from src.visual.palette import DEFAULT_PALETTE
from src.visual.utils.asset_manager import AssetManager


class GameComponent:
    """A base class for all game components.

    Attributes:
        parent (GameComponent | None): The parent component of this component.
        children (list[GameComponent]): A list of children.
        paused (bool): A flag indicating whether the component is paused.
        hidden (bool): A flag indicating whether the component is hidden.

    """

    def __init__(self) -> None:
        """Initialize a GameComponent instance."""
        self.parent: "GameComponent | None" = None
        self.children: "list[GameComponent]" = []
        self.paused = False
        self.hidden = False

    @final
    def update(self, delta: float) -> None:
        """Update the component and its children.

        Args:
            delta (float): The time elapsed since the last update.

        """
        if self.paused:
            return

        self._on_update(delta)
        for child in self.children:
            child.update(delta)

    def _on_update(self, delta: float) -> None:
        """Override to update component.

        Args:
            delta (float): The time elapsed since the last update.

        """
        pass

    @final
    def handle_input(self, event: Event) -> None | Event:
        """Handle input for component and its children.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event to propagate to the parent, or None.

        """
        if self.hidden:
            return event

        propagate_event = True

        for child in self.children[::-1]:
            ret = child.handle_input(event)
            if ret is None:
                return

        if propagate_event:
            return self._on_input(event)

    def _on_input(self, event: Event) -> Event | None:
        """Override to handle input for component.

        Args:
            event (Event): The input event to handle.

        Returns:
            Event | None: The event to propagate to the parent, or None.

        """
        return event

    @final
    def add_child(self, child: "GameComponent") -> None:
        """Add a child component to this one.

        Args:
            child (GameComponent): The child component to add.

        """
        self.children.append(child)
        child.parent = self

    @final
    def remove_child(self, child: "GameComponent") -> None:
        """Remove a child component from this one.

        Args:
            child (GameComponent): The child component to remove.

        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    @final
    def free_from_scene(self) -> None:
        """Remove a child component to this one."""
        if self.parent is not None:
            self.parent.remove_child(self)

    def clear_children(self) -> None:
        """Remove a child component to this one."""
        self.children.clear()


class Node(GameComponent):
    """A base class for all game nodes.

    Attributes:
        local_position (Vector2): The position relative to its parent.
        context (Context): The context of the game.

    """

    def __init__(self, context: "Context") -> None:
        """Initialize a Node instance."""
        super().__init__()
        self.local_position: Vector2 = Vector2()
        self.context = context

    @property
    def world_position(self) -> Vector2:
        """Get the absolute world position from relative parent positions."""
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

    @final
    def redraw(self) -> None:
        """Handle redrawing the visuals of a component and it's children."""
        self._on_redraw()

        for child in self.children:
            if isinstance(child, Node):
                child.redraw()

    def _on_redraw(self) -> None:
        """Override to redraw component."""
        ...


class Context:
    """A class that holds the context of the game.

    Attributes:
        screen (Surface): The Pygame surface to draw on.
        width (int): The width of the game window.
        height (int): The height of the game window.
        assets (AssetManager): The asset manager for managing assets.
        user_manager (UserManager): The user manager for handling user data.
        colors (dict[str, tuple[int, int, int]]): color names and their RGB.
        game_running (bool): A flag indicating whether the game is running.
        root_scene (RootScene): The root scene of the game.

    """

    def __init__(
        self,
        screen: Surface,
        width: int,
        height: int,
        assets: AssetManager,
        user_manager: UserManager,
        config: Config
    ) -> None:
        """Initialize a Context instance."""
        from src.visual.scenes.root import RootScene

        self.screen = screen
        self.width = width
        self.height = height
        self.assets = assets
        self.user_manager = user_manager
        self.colors = DEFAULT_PALETTE
        self.game_running = True
        self.root_scene = RootScene(self)
        self.config = config
