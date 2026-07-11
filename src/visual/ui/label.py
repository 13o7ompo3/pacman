import pygame
from src.visual import Context, Node
from pygame import Color, Rect, Surface, Vector2, draw, transform


class Label(Node):
    def __init__(
        self,
        context: Context,
        box_size: Vector2,
        texts: list[tuple[str, Color]],
        scale: int = 1,
        background_color: Color = Color(0, 0, 0, 0),
        border_color: Color = Color(0, 0, 0, 0),
        border_width: int = 0,
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

        draw.rect(
            self.text,
            background_color,
            Rect(Vector2(), label_size),
            0,
            border_radius,
        )
        if border_width > 0:
            draw.rect(
                self.text,
                border_color,
                Rect(Vector2(), label_size),
                border_width,
                border_radius,
            )
        self.text.blit(text, label_size / 2 - text_size / 2)

    def _on_draw(self) -> None:
        self.context.screen.blit(self.text, self.world_position)
