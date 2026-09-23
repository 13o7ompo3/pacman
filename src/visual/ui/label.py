"""A module that defines a Label class."""

import pygame
from pygame import Color, Surface, transform


from src.visual import Context, Node
from src.visual.draw import Draw
from src.visual.utils.primitives import Vec2
from src.visual.utils.font import Font


class Label(Node):
    """A class that represents a label.

    Attributes:
        box_size (Vec2): The size of the label box.
        texts (list[tuple[str, Color]]): A list of tuples of text and color.
        scale (int): The scale factor for the text.
        background_color (Color | None): The background color of the label.
        border_color (Color | None): The border color of the label.
        border_radius (int): The radius of the label's border corners.

    """

    def __init__(
        self,
        context: Context,
        box_size: Vec2,
        texts: list[tuple[str, Color]],
        scale: int = 1,
        background_color: Color | None = None,
        border_color: Color | None = None,
        border_radius: int = 0,
        font: Font | None = None,
    ) -> None:
        """Initialize a Label instance.

        Args:
            context (Context): The context in which the label exists.
            box_size (Vec2): The size of the label box.
            texts (list[tuple[str, Color]]): A list of tuples of (text, color).
            scale (int): The scale factor for the text.
            background_color (Color | None): The background color of the label.
            border_color (Color | None): The border color of the label.
            border_radius (int): The radius of the label's border corners.
            font (Font | None): The font to use for the label text.
        """
        super().__init__(context)
        self.box_size = box_size
        self.texts = texts
        self.scale = scale
        self.background_color = background_color
        self.border_color = border_color
        self.border_radius = border_radius
        if font:
            self.font = font
        else:
            self.font = context.assets.font("ui")

        self.text: Surface

        self._on_redraw()

    def _on_draw(self) -> None:
        """Draw the label on the screen."""
        self.context.screen.blit(self.text, self.world_position.as_tuple())

    def get_as_surface(self) -> Surface:
        """Get the label as a Pygame Surface.

        Returns:
            Surface: The label as a Pygame Surface.

        """
        return self.text

    def _on_redraw(self) -> None:
        """Redraw the label."""
        text_surfaces = []
        min_size = Vec2()
        for text, color in self.texts:
            surface = self.font.render(text, False, color).convert_alpha()
            text_surfaces.append(surface)
            min_size.y = max(min_size.y, surface.get_size()[1])
            min_size.x += surface.get_size()[0]

        text_surf = Surface(min_size.as_tuple(), pygame.SRCALPHA)
        offset = Vec2()
        for surface in text_surfaces:
            text_surf.blit(surface, offset.as_tuple())
            offset.x += surface.get_size()[0]

        text_surf = transform.scale_by(text_surf, self.scale)
        text_size = Vec2(text_surf.get_size())

        label_size = Vec2(
            max(self.box_size.x, text_size.x),
            max(self.box_size.y, text_size.y),
        )
        self.text = Surface(label_size.as_tuple(), pygame.SRCALPHA)

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
        self.text.blit(
            text_surf,
            (label_size / 2 - text_size / 2).as_tuple(),
        )
