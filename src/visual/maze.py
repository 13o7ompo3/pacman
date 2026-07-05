from pydantic import BaseModel

from src.visual import Node


class VisualMaze(Node, BaseModel):
    pass
