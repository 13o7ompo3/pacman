from pydantic import BaseModel
from pygame import Surface
from pygame.event import Event

from src.visual import DrawableComponent


class Screen(DrawableComponent):
    def update(self, delta: float, event: Event) -> None:
        pass

    def render(self, screen: Surface) -> None:
        pass
