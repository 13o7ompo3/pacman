import pygame
from src.visual import Context, Node
from pygame import Color, Rect, Surface, Vector2, draw, transform
from src.visual.draw import Draw


class Label(Node):
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
        super().__init__(context)

        text_surfaces = []
        min_size = Vector2()
        for text, color in texts:
            surface = context.font.render(text, False, color).convert_alpha()
            text_surfaces.append(surface)
            min_size.y = max(min_size.y, surface.get_size()[1])
            min_size.x += surface.get_size()[0]

        text = Surface(min_size, pygame.SRCALPHA)
        offset = Vector2()
        for surface in text_surfaces:
            text.blit(surface, offset)
            offset.x += surface.get_size()[0]

        text = transform.scale_by(text, scale)
        text_size = Vector2(text.get_size())

        label_size = Vector2(
            max(box_size.x, text_size.x),
            max(box_size.y, text_size.y),
        )
        self.text = Surface(label_size, pygame.SRCALPHA)

        self.size = box_size
        if background_color:
            Draw.rect(
                self.text,
                background_color,
                (0, 0),
                label_size,
                True,
                border_radius,
            )
        if border_color:
            Draw.rect(
                self.text,
                border_color,
                (0, 0),
                label_size,
                False,
                border_radius,
            )
        self.text.blit(text, label_size / 2 - text_size / 2)

    def _on_draw(self) -> None:
        self.context.screen.blit(self.text, self.world_position)

    def get_as_surface(self) -> Surface:
        return self.text
