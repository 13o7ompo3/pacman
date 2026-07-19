from pygame import Surface, PixelArray, Vector2, Color


class Draw:
    cache: dict = {}

    @staticmethod
    def rect(
        surface: Surface,
        position: Vector2 | tuple[int, int],
        size: Vector2 | tuple[int, int],
        color: Color | tuple[int, int, int],
        border_width: int = 0,
        border_radius: int = 0,
    ):
        if isinstance(position, Vector2):
            position = (int(position.x), int(position.y))
        if isinstance(size, Vector2):
            size = (int(size.x), int(size.y))
        if isinstance(color, Color):
            color = (color.r, color.g, color.b)

        cache_key = (size, color, border_width, border_radius)

        if cache_key not in Draw.cache:
            rect = Surface(size)
            array = PixelArray(rect)

            for x in range(size[0]):
                for y in range(size[1]):
                    array[x, y] = color

            array.close()
            Draw.cache[cache_key] = rect
        else:
            rect = Draw.cache[cache_key]

        Draw.cache[cache_key] = rect

        surface.blit(rect, position)
