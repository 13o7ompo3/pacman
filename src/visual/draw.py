from pygame import Surface, PixelArray, Vector2, Color
import math
import pygame


class Draw:
    cache: dict = {}

    @staticmethod
    def rect(
        surface: Surface,
        color: Color | tuple[int, int, int],
        position: Vector2 | tuple[int, int],
        size: Vector2 | tuple[int, int],
        filled: bool,
        border_radius: int = 0,
    ):
        if isinstance(position, Vector2):
            position = (int(position.x), int(position.y))
        if isinstance(size, Vector2):
            size = (int(size.x), int(size.y))
        if isinstance(color, Color):
            color = (color.r, color.g, color.b)

        cache_key = ("rect", size, color, filled, border_radius)

        if cache_key not in Draw.cache:
            rect = Surface(size, flags=pygame.SRCALPHA)
            array = PixelArray(rect)

            for x in range(size[0]):
                for y in range(size[1]):
                    if filled:
                        array[x, y] = color
                    elif (
                        x == 0
                        or x == size[0] - 1
                        or y == 0
                        or y == size[1] - 1
                    ):
                        array[x, y] = color

            array.close()
            Draw.cache[cache_key] = rect
        else:
            rect = Draw.cache[cache_key]

        surface.blit(rect, position)

    @staticmethod
    def sector(
        surface: Surface,
        color: Color | tuple[int, int, int],
        position: Vector2 | tuple[int, int],
        radius: int,
        start_angle: float,
        end_angle: float,
        filled: bool,
    ):
        if isinstance(position, Vector2):
            position = (int(position.x) - radius, int(position.y) - radius)
        if isinstance(color, Color):
            color = (color.r, color.g, color.b)

        cache_key = (
            "sector",
            color,
            position,
            radius,
            start_angle,
            end_angle,
            filled,
        )

        if cache_key not in Draw.cache:
            size = (radius * 2 + 1, radius * 2 + 1)
            rect = Surface(size, flags=pygame.SRCALPHA)
            array = PixelArray(rect)

            for x in range(-radius, radius + 1):
                for y in range(-radius, radius + 1):
                    length = round(math.sqrt((x) ** 2 + (y) ** 2))
                    angle = math.atan2(y, -x)
                    in_sector = start_angle <= angle + math.pi <= end_angle
                    if filled and (length <= radius) and in_sector:
                        array[x + radius, y + radius] = color
                    elif (length == radius) and in_sector:
                        array[x + radius, y + radius] = color

            array.close()
            Draw.cache[cache_key] = rect
        else:
            rect = Draw.cache[cache_key]

        surface.blit(rect, position)

    @staticmethod
    def rounded_rect(
        surface: Surface,
        color: Color | tuple[int, int, int],
        position: Vector2 | tuple[int, int],
        size: Vector2 | tuple[int, int],
        filled: bool,
        radius: int = 0,
    ):
        if isinstance(position, Vector2):
            position = (int(position.x), int(position.y))
        if isinstance(size, Vector2):
            size = (int(size.x), int(size.y))
        if isinstance(color, Color):
            color = (color.r, color.g, color.b)

        radius = min(radius, size[0] // 2, size[1] // 2)

        if filled:
            Draw.rect(
                surface,
                color,
                (position[0] + radius, position[1]),
                (size[0] - 2 * radius, size[1] + 1),
                filled,
            )
            Draw.rect(
                surface,
                color,
                (position[0], position[1] + radius),
                (size[0] + 1, size[1] - 2 * radius + 1),
                filled,
            )
        else:
            Draw.rect(
                surface,
                color,
                (position[0] + radius, position[1]),
                (size[0] - 2 * radius, 1),
                filled,
            )
            Draw.rect(
                surface,
                color,
                (position[0] + radius, position[1] + size[1]),
                (size[0] - 2 * radius, 1),
                filled,
            )
            Draw.rect(
                surface,
                color,
                (position[0], position[1] + radius),
                (1, size[1] - 2 * radius),
                filled,
            )
            Draw.rect(
                surface,
                color,
                (position[0] + size[0], position[1] + radius),
                (1, size[1] - 2 * radius),
                filled,
            )

        Draw.sector(
            surface,
            color,
            (position[0], position[1]),
            radius,
            0.5 * math.pi,
            1 * math.pi,
            filled,
        )
        Draw.sector(
            surface,
            color,
            (position[0] + size[0] - 2 * radius, position[1]),
            radius,
            0 * math.pi,
            0.5 * math.pi,
            filled,
        )
        Draw.sector(
            surface,
            color,
            (
                position[0] + size[0] - 2 * radius,
                position[1] + size[1] - 2 * radius,
            ),
            radius,
            1.5 * math.pi,
            2 * math.pi,
            filled,
        )
        Draw.sector(
            surface,
            color,
            (position[0], position[1] + size[1] - 2 * radius),
            radius,
            1 * math.pi,
            1.5 * math.pi,
            filled,
        )
