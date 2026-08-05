"""A module that defines a Label class."""

import pygame
from src.visual import Context, Node
from pygame import Color, Surface, Vector2, transform
from src.visual.draw import Draw


class Label(Node):
    """A class that represents a label.

    Attributes:
        box_size (Vector2): The size of the label box.
        texts (list[tuple[str, Color]]): A list of tuples of text and color.
        scale (int): The scale factor for the text.
        background_color (Color | None): The background color of the label.
        border_color (Color | None): The border color of the label.
        border_radius (int): The radius of the label's border corners.

    """

    def __init__(
        self,
        context: Context,
        box_size: Vector2,
        texts: list[tuple[str, Color]],
        scale: int = 1,
        background_color: Color | None = None,
        border_color: Color | None = None,
        border_radius: int = 0,
    ) -> None:
        """Initialize a Label instance."""
        super().__init__(context)
        self.box_size = box_size
        self.texts = texts
        self.scale = scale
        self.background_color = background_color
        self.border_color = border_color
        self.border_radius = border_radius

        self._on_redraw()

    def _on_draw(self) -> None:
        """Draw the label on the screen."""
        self.context.screen.blit(self.text, self.world_position)

    def get_as_surface(self) -> Surface:
        """Get the label as a Pygame Surface.

        Returns:
            Surface: The label as a Pygame Surface.

        """
        return self.text

    def _on_redraw(self) -> None:
        """Redraw the label."""
        text_surfaces = []
        min_size = Vector2()
        for text, color in self.texts:
            surface = (
                self.context.assets.font("ui")
                .render(text, False, color)
                .convert_alpha()
            )
            text_surfaces.append(surface)
            min_size.y = max(min_size.y, surface.get_size()[1])
            min_size.x += surface.get_size()[0]

        text = Surface(min_size, pygame.SRCALPHA)
        offset = Vector2()
        for surface in text_surfaces:
            text.blit(surface, offset)
            offset.x += surface.get_size()[0]

        text = transform.scale_by(text, self.scale)
        text_size = Vector2(text.get_size())

        label_size = Vector2(
            max(self.box_size.x, text_size.x),
            max(self.box_size.y, text_size.y),
        )
        self.text = Surface(label_size, pygame.SRCALPHA)

        self.size = label_size
        Draw.rect(
            self.text,
            (0, 0),
            label_size,
            self.background_color,
            self.border_color,
            1,
            self.border_radius,
        )
        self.text.blit(text, label_size / 2 - text_size / 2)
