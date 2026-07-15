from src.visual import Node, Context
from src.visual.scenes.game.maze import VisualMaze
from src.visual.ui.progress import ProgressBar, ProgressBarOrientation
from pygame import Color, Vector2, draw

from src.visual.ui.button import Button
from src.visual.scenes.pause import PauseScene


class GameScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        maze = VisualMaze(context)
        self.maze = maze
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

        self.progress = ProgressBar(
            context,
            Vector2(maze.size.x, 32),
            ProgressBarOrientation.HORIZONTAL,
            Color("teal"),
            border_radius=10,
            total=len(maze.logical_maze.pacgums),
            reversed=True,
        )
        self.progress.local_position = Vector2(
            maze.world_position.x, maze.world_position.y - 50
        )

        self.add_child(maze)
        self.add_child(pause_button)
        self.add_child(self.progress)

    def _on_update(self, delta: float) -> None:
        self.progress.progress = len(self.maze.logical_maze.pacgums)
