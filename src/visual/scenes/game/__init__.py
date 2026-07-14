from src.visual import Node, Context
from src.visual.scenes.game.maze import VisualMaze
from pygame import Color, Vector2, draw

from src.visual.ui.button import Button
from src.visual.scenes.pause import PauseScene


class GameScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        maze = VisualMaze(context)
        maze.local_position = (
            Vector2(context.width, context.height) / 2 - maze.size / 2
        )

        pause_button = Button(
            context,
            "=",
            Vector2(30, 30),
            Color("white"),
            lambda: context.root_scene.add_child(PauseScene(context, maze)),
        )

        self.add_child(maze)
        self.add_child(pause_button)

    def _on_draw(self) -> None:
        draw.line(
            self.context.screen,
            Color("pink"),
            Vector2(self.context.width, 0) / 2,
            Vector2(self.context.width, self.context.height) / 2,
        )
