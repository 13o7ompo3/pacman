from pygame import Surface
from src.visual import Node, Context


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
        self.time = 0

    def _on_update(self, delta: float) -> None:
        self.time += delta

    def _on_draw(self) -> None:
        # self.context.screen.blit()
        pass

    def play(self):
        pass

    def stop(self):
        pass
