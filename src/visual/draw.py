from pygame import Surface, PixelArray, Vector2, Color
import math
import pygame


class Draw:
    cache: dict = {}

    @staticmethod
    def rect(
        surface: Surface,
        position: Vector2 | tuple[int, int],
        size: Vector2 | tuple[int, int],
        fill_color: Color | tuple[int, int, int] | None = None,
        border_color: Color | tuple[int, int, int] | None = None,
        border_width: int = 0,
        border_radius: int = 0,
    ):
        if isinstance(position, Vector2):
            position = (int(position.x), int(position.y))
        if isinstance(size, Vector2):
            size = (int(size.x), int(size.y))
        if isinstance(fill_color, Color):
            fill_color = (fill_color.r, fill_color.g, fill_color.b)
        if isinstance(border_color, Color):
            border_color = (border_color.r, border_color.g, border_color.b)

        cache_key = (
            "rect",
            size,
            fill_color,
            border_color,
            border_width,
            border_radius,
        )

        if cache_key not in Draw.cache:
            rect = Surface((size[0], size[1]), flags=pygame.SRCALPHA)

            if fill_color:
                if border_radius == 0:
                    Draw._rect_filled(rect, (0, 0), size, fill_color)
                elif border_radius > 0:
                    Draw._rect_round(
                        rect,
                        (0, 0),
                        size,
                        border_width,
                        border_radius,
                        True,
                        fill_color,
                    )

            if border_color and border_width > 0:
                if border_radius == 0:
                    Draw._rect_outline(
                        rect, (0, 0), size, border_color, border_width
                    )
                elif border_radius > 0:
                    Draw._rect_round(
                        rect,
                        (0, 0),
                        size,
                        border_width,
                        border_radius,
                        False,
                        border_color,
                    )

            Draw.cache[cache_key] = rect
        else:
            rect = Draw.cache[cache_key]

        surface.blit(rect, position)

    @staticmethod
    def _rect_filled(
        surface: Surface,
        position: tuple[int, int],
        size: tuple[int, int],
        color: tuple[int, int, int],
    ) -> None:
        array = PixelArray(surface)
        for x in range(position[0], size[0] + position[0]):
            for y in range(position[1], size[1] + position[1]):
                array[x, y] = color
        array.close()

    @staticmethod
    def _rect_outline(
        surface: Surface,
        position: tuple[int, int],
        size: tuple[int, int],
        color: tuple[int, int, int],
        border_width: int,
    ) -> None:
        min_x_bound = position[0]
        max_x_bound = size[0] + position[0] - 1
        min_y_bound = position[1]
        max_y_bound = size[1] + position[1] - 1
        array = PixelArray(surface)
        for x in range(position[0], size[0] + position[0]):
            for y in range(position[1], size[1] + position[1]):
                if (
                    (min_x_bound <= x < min_x_bound + border_width)
                    or (max_x_bound - border_width < x <= max_x_bound)
                    or (min_y_bound <= y < min_y_bound + border_width)
                    or (max_y_bound - border_width < y <= max_y_bound)
                ):
                    array[x, y] = color
        array.close()

    @staticmethod
    def sector(
        surface: Surface,
        color: Color | tuple[int, int, int],
        position: Vector2 | tuple[int, int],
        border_width: int,
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
                    length = math.sqrt((x) ** 2 + (y) ** 2)
                    angle = math.atan2(y, -x)
                    in_sector = start_angle <= angle + math.pi <= end_angle
                    if filled and (length <= radius) and in_sector:
                        array[x + radius, y + radius] = color
                    elif (
                        radius - border_width <= length <= radius
                    ) and in_sector:
                        array[x + radius, y + radius] = color

            array.close()
            Draw.cache[cache_key] = rect
        else:
            rect = Draw.cache[cache_key]

        surface.blit(rect, position)

    @staticmethod
    def _rect_round(
        surface: Surface,
        position: tuple[int, int],
        size: tuple[int, int],
        border_width: int,
        radius: int,
        filled: bool,
        color: tuple[int, int, int],
    ) -> None:
        radius = min(radius, size[0] // 2, size[1] // 2)

        if filled:
            Draw._rect_filled(
                surface,
                (position[0] + radius, position[1]),
                (size[0] - 2 * radius, size[1]),
                color,
            )
            Draw._rect_filled(
                surface,
                (position[0], position[1] + radius),
                (size[0], size[1] - 2 * radius),
                color,
            )
        else:
            min_x_bound = position[0]
            max_x_bound = size[0] + position[0] - 1
            min_y_bound = position[1]
            max_y_bound = size[1] + position[1] - 1

            array = PixelArray(surface)
            for x in range(position[0], size[0] + position[0]):
                for y in range(position[1], size[1] + position[1]):
                    in_left_border = (
                        min_x_bound <= x < min_x_bound + border_width
                    ) and radius <= y <= max_y_bound - radius
                    in_right_border = (
                        max_x_bound - border_width < x <= max_x_bound
                    ) and radius <= y <= max_y_bound - radius
                    in_top_border = (
                        min_y_bound <= y < min_y_bound + border_width
                    ) and radius <= x <= max_x_bound - radius
                    in_bottom_border = (
                        max_y_bound - border_width < y <= max_y_bound
                    ) and radius <= x <= max_x_bound - radius

                    if any(
                        (
                            in_left_border,
                            in_right_border,
                            in_top_border,
                            in_bottom_border,
                        )
                    ):
                        array[x, y] = color
            array.close()

        Draw.sector(
            surface,
            color,
            position,
            border_width,
            radius,
            0.5 * math.pi,
            1 * math.pi,
            filled,
        )
        Draw.sector(
            surface,
            color,
            (position[0] + size[0] - 2 * radius - 1, position[1]),
            border_width,
            radius,
            0 * math.pi,
            0.5 * math.pi,
            filled,
        )
        Draw.sector(
            surface,
            color,
            (
                position[0] + size[0] - 2 * radius - 1,
                position[1] + size[1] - 2 * radius - 1,
            ),
            border_width,
            radius,
            1.5 * math.pi,
            2 * math.pi,
            filled,
        )
        Draw.sector(
            surface,
            color,
            (position[0], position[1] + size[1] - 2 * radius - 1),
            border_width,
            radius,
            1 * math.pi,
            1.5 * math.pi,
            filled,
        )
