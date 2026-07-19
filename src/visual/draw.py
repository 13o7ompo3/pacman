from pygame import Surface, PixelArray, Vector2, Color
import math


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
            rect = Surface(size)
            array = PixelArray(rect)

            Draw._rect_filled(array, color, size)

            array.close()
            Draw.cache[cache_key] = rect
        else:
            rect = Draw.cache[cache_key]

        surface.blit(rect, position)

    @staticmethod
    def _rect_filled(array: PixelArray, color: Color, size: tuple) -> None:
        for x in range(size[0]):
            for y in range(size[1]):
                array[x, y] = color

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
            rect = Surface(size)
            array = PixelArray(rect)

            for x in range(size[0]):
                for y in range(size[1]):
                    length = round(
                        math.sqrt((x - radius) ** 2 + (y - radius) ** 2)
                    )
                    angle = math.atan2(x - radius, y - radius)
                    in_sector = start_angle < angle <= end_angle
                    if filled and (length <= radius) and in_sector:
                        array[x, y] = color
                    elif (length == radius) and in_sector:
                        array[x, y] = color

            array.close()
            Draw.cache[cache_key] = rect
        else:
            rect = Draw.cache[cache_key]

        surface.blit(rect, position)
