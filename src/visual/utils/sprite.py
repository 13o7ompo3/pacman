from pygame import Surface
import pygame
from src.visual import Node, Context
from src.visual.draw import Draw
from src.visual.utils.image import Image
from typing import Dict, Tuple


class Sprite(Node):
    def __init__(
        self,
        context: Context,
        surface: Surface,
        rows: int,
        cols: int,
        fps: int,
        repeat: bool,
    ) -> None:
        super().__init__(context)
        self.fps = fps
        self.time = 0.0
        self.rows = rows
        self.cols = cols
        self.repeat = repeat
        self.frames = Image.split_surface(surface, self.rows, self.cols)
        self.flipped_frames = self.__compute_flipped_frames()
        self.current_frame_index = 0
        self.playing = True
        self.flip_x = False
        self.flip_y = False

    def __compute_flipped_frames(
        self,
    ) -> Dict[Tuple[bool, bool], list[Surface]]:
        flipped_frames: Dict[Tuple[bool, bool], list[Surface]] = {}
        for flip_x in [False, True]:
            for flip_y in [False, True]:
                flipped_frames[(flip_x, flip_y)] = []
                for frame in self.frames:
                    flipped_frames[(flip_x, flip_y)].append(
                        Image.flip_surface(frame, flip_x, flip_y)
                    )
        return flipped_frames

    def _on_update(self, delta: float) -> None:
        if not self.playing:
            return
        self.time += delta
        if self.time >= 1.0 / self.fps:
            self.current_frame_index += int(self.time * self.fps)
            self.time = 0.0
            if self.current_frame_index >= len(self.frames):
                if self.repeat:
                    self.current_frame_index = 0
                else:
                    self.current_frame_index = len(self.frames) - 1

    def _on_draw(self) -> None:
        self.frames = self.flipped_frames[(self.flip_x, self.flip_y)]
        current_frame = self.frames[self.current_frame_index]
        self.context.screen.blit(
            current_frame,
            (
                self.world_position.x - current_frame.get_width() / 2,
                self.world_position.y - current_frame.get_height() / 2,
            ),
        )

    def flip(self, flip_x: bool, flip_y: bool) -> None:
        self.flip_x = flip_x
        self.flip_y = flip_y

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False
