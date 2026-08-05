"""This module provides utility classes and functions
for handling sprites and animations in Pygame."""
from pygame import Surface
from src.visual import Node, Context
from src.visual.utils.image import Image
from typing import Dict, Tuple


class Sprite(Node):
    """A class representing a sprite with animation capabilities."""
    def __init__(
        self,
        context: Context,
        surface: Surface,
        rows: int,
        cols: int,
        fps: int,
        repeat: bool,
    ) -> None:
        """Initialize a Sprite instance.

        Args:
            context (Context): The context in which the sprite exists.
            surface (Surface): The surface representing the sprite's image.
            rows (int): The number of rows in the sprite sheet.
            cols (int): The number of columns in the sprite sheet.
            fps (int): The frames per second for the animation.
            repeat (bool): Whether the animation should repeat after finishing.
        """
        super().__init__(context)
        self.fps = fps
        self.time = 0.0
        self.rows = rows
        self.cols = cols
        self.repeat = repeat
        self.surface = surface
        self.frames: list[Surface] = []
        self.flipped_frames: Dict[Tuple[bool, bool], list[Surface]] = {}
        self._on_redraw()
        self.current_frame_index = 0
        self.playing = True
        self.flip_x = False
        self.flip_y = False

    def __compute_flipped_frames(
        self,
    ) -> Dict[Tuple[bool, bool], list[Surface]]:
        """Compute and return a dictionary of flipped frames for the sprite.

        Returns:
            Dict[Tuple[bool, bool], list[Surface]]: A dictionary where
              the keys are tuples representing the flip state (flip_x, flip_y)
              and the values are lists of surfaces representing
              the corresponding flipped frames.
        """
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
        """Update the sprite's animation based on the elapsed time.

        Args:
            delta (float): The time elapsed since the last update, in seconds.
        """
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
        """Draw the current frame of the sprite on the screen."""
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
        """Set the flip state for the sprite's animation.

        Args:
            flip_x (bool): Whether to flip the sprite horizontally.
            flip_y (bool): Whether to flip the sprite vertically.
        """
        self.flip_x = flip_x
        self.flip_y = flip_y

    def play(self):
        """Start or resume the sprite's animation."""
        self.playing = True

    def stop(self):
        """Stop the sprite's animation."""
        self.playing = False

    def _on_redraw(self) -> None:
        """Split the sprite sheet into individual frames
            and compute flipped frames."""
        self.frames = Image.split_surface(self.surface, self.rows, self.cols)
        self.flipped_frames = self.__compute_flipped_frames()
