from src.visual import Node, Context
from src.visual.scenes.game.maze import VisualMaze
from pygame import Color, Vector2

from src.visual.ui.button import Button
from src.visual.scenes.pause import PauseScene


class GameScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        maze = VisualMaze(context)
        maze.local_position = Vector2(100, 100)

        pause_button = Button(
            context,
            "=",
            Vector2(30, 30),
            Color("white"),
            lambda: context.root_scene.add_child(PauseScene(context, maze)),
        )

        self.add_child(maze)
        self.add_child(pause_button)
