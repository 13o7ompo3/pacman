"""
This module provides utility functions for image manipulation using Pygame.
"""

import pygame
from pygame import Surface, Color
from typing import Tuple
import numpy as np
from src.visual.palette import ColorPalette


class Image:
    """
    A utility class for image manipulation using Pygame.
    """

    @staticmethod
    def subsurface(
        surface: Surface, x: int, y: int, width: int, height: int
    ) -> Surface:
        """
        Create a subsurface from the given surface.

        Args:
            surface (Surface): The parent surface.
            x (int): The x-coordinate of the top-left corner of the subsurface.
            y (int): The y-coordinate of the top-left corner of the subsurface.
            width (int): The width of the subsurface.
            height (int): The height of the subsurface.
        Returns:
            Surface: A new surface representing the subsurface.
        """
        parent_width, parent_height = surface.get_size()
        if x < 0 or y < 0 or width <= 0 or height <= 0:
            raise ValueError(
                "Subsurface rectangle dimensions must be positive."
            )
        if x + width > parent_width or y + height > parent_height:
            raise ValueError(
                "Subsurface rectangle outside parent surface area."
            )
        child_surface = pygame.Surface(
            (width, height),
            flags=surface.get_flags(),
            depth=surface.get_bitsize(),
        )
        with pygame.PixelArray(surface) as parent_array:
            with pygame.PixelArray(child_surface) as child_array:
                child_array[:] = parent_array[x : x + width, y : y + height]  # type: ignore[index]
        return child_surface

    @staticmethod
    def flip_surface(surface: Surface, flip_x: bool, flip_y: bool) -> Surface:
        """
        Flip the given surface horizontally and/or vertically.

        Args:
            surface (Surface): The surface to flip.
            flip_x (bool): Whether to flip horizontally.
            flip_y (bool): Whether to flip vertically.
        Returns:
            Surface: A new surface that is the flipped version of the original.
        """
        width = surface.get_width()
        height = surface.get_height()
        flipped_surface = pygame.Surface(
            (width, height),
            flags=surface.get_flags(),
            depth=surface.get_bitsize(),
        )
        with pygame.PixelArray(surface) as original_array:
            with pygame.PixelArray(flipped_surface) as flipped_array:
                x_slice = slice(None, None, -1) if flip_x else slice(None)
                y_slice = slice(None, None, -1) if flip_y else slice(None)

                flipped_array[:] = original_array[x_slice, y_slice]  # type: ignore[index]
        return flipped_surface

    @staticmethod
    def split_surface(surface: Surface, rows: int, cols: int) -> list[Surface]:
        """
        Split a surface into a grid of smaller surfaces.

        Args:
            surface (Surface): The surface to split.
            rows (int): The number of rows in the grid.
            cols (int): The number of columns in the grid.
        Returns:
            list[Surface]: A list of subsurfaces representing the grid cells.
        """
        width, height = surface.get_size()
        frame_width = width // cols
        frame_height = height // rows
        frames = []
        for row in range(rows):
            for col in range(cols):
                frame_rect = (
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height,
                )
                frame_surface = Image.subsurface(surface, *frame_rect)
                frames.append(frame_surface)
        return frames

    @staticmethod
    def blit(
        dest_surface: Surface,
        source_surface: Surface,
        position: Tuple[int, int] | Tuple[float, float] | pygame.Vector2,
    ) -> None:
        if isinstance(position, pygame.Vector2):
            position = position.x, position.y

        x, y = (int(position[0]), int(position[1]))
        src_w, src_h = source_surface.get_width(), source_surface.get_height()
        dst_w, dst_h = dest_surface.get_width(), dest_surface.get_height()

        x1_dst = max(0, x)
        y1_dst = max(0, y)
        x2_dst = min(dst_w, x + src_w)
        y2_dst = min(dst_h, y + src_h)

        if x1_dst >= x2_dst or y1_dst >= y2_dst:
            return

        x1_src = x1_dst - x
        y1_src = y1_dst - y
        x2_src = x1_src + (x2_dst - x1_dst)
        y2_src = y1_src + (y2_dst - y1_dst)

        has_dst_alpha = dest_surface.get_flags() & pygame.SRCALPHA

        src_pixels = pygame.surfarray.pixels3d(source_surface)
        src_alpha = pygame.surfarray.array_alpha(source_surface)
        dst_pixels = pygame.surfarray.pixels3d(dest_surface)

        src_slice_rgb = src_pixels[x1_src:x2_src, y1_src:y2_src]
        src_slice_a = src_alpha[x1_src:x2_src, y1_src:y2_src]
        dst_slice_rgb = dst_pixels[x1_dst:x2_dst, y1_dst:y2_dst]

        alpha_normalized = src_slice_a[..., np.newaxis] / 255.0

        if has_dst_alpha:
            dst_alpha = pygame.surfarray.pixels_alpha(dest_surface)
            dst_slice_a = dst_alpha[x1_dst:x2_dst, y1_dst:y2_dst]

            blended_rgb = src_slice_rgb * alpha_normalized + dst_slice_rgb * (
                1.0 - alpha_normalized
            )

            dst_slice_rgb[:] = blended_rgb.astype(np.uint8)
            dst_slice_a[:] = np.maximum(src_slice_a, dst_slice_a).astype(
                np.uint8
            )
        else:
            blended_rgb = src_slice_rgb * alpha_normalized + dst_slice_rgb * (
                1.0 - alpha_normalized
            )
            dst_slice_rgb[:] = blended_rgb.astype(np.uint8)

    @staticmethod
    def fill(surface: Surface, color: Tuple[int, int, int]) -> None:
        """
        Fill a surface with a solid color.

        Args:
            surface (Surface): The surface to fill.
            color (Tuple[int, int, int]): The RGB color to fill the surface
              with.
        Returns:
            None
        """
        pixel_array = pygame.surfarray.pixels3d(surface)
        pixel_array[:, :] = color

    @staticmethod
    def switch_palette(
        surface: Surface, old_palette: ColorPalette, new_palette: ColorPalette
    ) -> None:
        """
        Switch the colors of a surface from an old palette to a new palette.

        Args:
            surface (Surface): The surface whose colors are to be switched.
            old_palette (ColorPalette): The original color palette.
            new_palette (ColorPalette): The new color palette to switch to.
        Returns:
            None
        """
        pixel_array = pygame.surfarray.pixels3d(surface)

        color_mapping = {
            Image.rgb(old_palette.darkest): Image.rgb(new_palette.darkest),
            Image.rgb(old_palette.darker): Image.rgb(new_palette.darker),
            Image.rgb(old_palette.dark): Image.rgb(new_palette.dark),
            Image.rgb(old_palette.light): Image.rgb(new_palette.light),
            Image.rgb(old_palette.lighter): Image.rgb(new_palette.lighter),
            Image.rgb(old_palette.lightest): Image.rgb(new_palette.lightest),
        }

        for original_color, new_color in color_mapping.items():
            mask = np.all(pixel_array == original_color, axis=-1)
            pixel_array[mask] = new_color

    @staticmethod
    def rgb(color: Color) -> Tuple[int, int, int]:
        """
        Convert a Pygame Color object to an RGB tuple.

        Args:
            color (Color): The Pygame Color object to convert.
        Returns:
            Tuple[int, int, int]: A tuple representing the RGB values of the
              color.
        """
        return color.r, color.g, color.b
