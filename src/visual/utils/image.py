"""
This module provides utility functions for image manipulation using Pygame.
"""

import numpy as np
import pygame
from pygame import Color, Surface

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
        with (
            pygame.PixelArray(surface) as parent,
            pygame.PixelArray(child_surface) as child,
        ):
            child[:] = parent[x : x + width, y : y + height]  # type: ignore[index]
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
        with (
            pygame.PixelArray(surface) as original,
            pygame.PixelArray(flipped_surface) as flipped,
        ):
            x_slice = slice(None, None, -1) if flip_x else slice(None)
            y_slice = slice(None, None, -1) if flip_y else slice(None)

            flipped[:] = original[x_slice, y_slice]  # type: ignore[index]
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
    def fill(surface: Surface, color: Color | tuple[int, int, int]) -> None:
        """
        Fill a surface with a solid color.

        Args:
            surface (Surface): The surface to fill.
            color (Tuple[int, int, int]): The RGB color to fill the surface
              with.
        Returns:
            None
        """
        if isinstance(color, Color):
            color = Image.rgb(color)
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
    def rgb(color: Color) -> tuple[int, int, int]:
        """
        Convert a Pygame Color object to an RGB tuple.

        Args:
            color (Color): The Pygame Color object to convert.
        Returns:
            Tuple[int, int, int]: A tuple representing the RGB values of the
              color.
        """
        return color.r, color.g, color.b
