import pygame
from pygame import Surface
from typing import Dict, Tuple
import numpy as np

class Image:
    @staticmethod
    def subsurface(surface: Surface, x: int, y: int, width: int, height: int) -> Surface:
        parent_width, parent_height = surface.get_size()
        if x < 0 or y < 0 or width <= 0 or height <= 0:
            raise ValueError("Subsurface rectangle dimensions must be positive.")
        if x + width > parent_width or y + height > parent_height:
            raise ValueError("Subsurface rectangle outside parent surface area.")
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
        position: Tuple[int, int] | pygame.Vector2,
    ) -> None:
        if isinstance(position, pygame.Vector2):
            position = (int(position.x), int(position.y))

        x, y = position
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



        src_pixels = pygame.surfarray.pixels3d(source_surface)
        src_alpha = pygame.surfarray.array_alpha(source_surface)
        
        dst_pixels = pygame.surfarray.pixels3d(dest_surface)
        dst_alpha = pygame.surfarray.array_alpha(dest_surface)

        src_slice_rgb = src_pixels[x1_src:x2_src, y1_src:y2_src]
        src_slice_a = src_alpha[x1_src:x2_src, y1_src:y2_src]

        dst_slice_rgb = dst_pixels[x1_dst:x2_dst, y1_dst:y2_dst]
        dst_slice_a = dst_alpha[x1_dst:x2_dst, y1_dst:y2_dst]

        alpha_normalized = src_slice_a[..., np.newaxis] / 255.0

        blended_rgb = (src_slice_rgb * alpha_normalized + dst_slice_rgb * (1.0 - alpha_normalized))
        blended_a = np.maximum(src_slice_a, dst_slice_a)

        dst_slice_rgb[:] = blended_rgb.astype(np.uint8)
        dst_slice_a[:] = blended_a.astype(np.uint8)
