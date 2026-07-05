from pydantic import BaseModel
from pygame import Surface
from pygame.event import Event
from pygame import draw, Color

from src.visual import Node


class Scene(Node):
    def _on_update(self, delta: float) -> None:
        self.local_position.x += delta * 10

    def _on_draw(self, screen: Surface) -> None:
        draw.circle(screen, Color("cyan"), self.world_position, 20)
