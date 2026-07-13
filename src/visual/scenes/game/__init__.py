from src.visual import Node, Context
from src.visual.scenes.game.maze import VisualMaze


class GameScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        maze = VisualMaze(context)
        self.add_child(maze)
