import logging

import pygame
import math
from pygame.time import Clock
from pygame import Color, Vector2, Rect
from src.visual.draw import Draw

from src.db_manager.user import UserManager
from src.visual import Context, GameComponent, Node
from src.visual.scenes.game import VisualMaze
from src.visual.scenes.title import TitleScene
from src.visual.ui.progress import ProgressBar, ProgressBarOrientation
from src.visual.ui.text_box import TextBox

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font("assets/perfect_dos_vga_437.ttf", 16)

    WIDTH, HEIGHT = 960, 600
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

    user_manager = UserManager()
    context = Context(surface, WIDTH, HEIGHT, font, user_manager)
    title_scene = TitleScene(context)
    context.root_scene.add_child(title_scene)

    clock = Clock()
    while context.game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and event.key in {pygame.K_ESCAPE, pygame.K_q}
            ):
                context.game_running = False

            context.root_scene.handle_input(event)

        # update the scene tree
        delta = clock.tick() / 1000
        context.root_scene.update(delta)

        # render the scene tree
        surface.fill(Color("black"))
        context.root_scene.render()

        Draw.rounded_rect(
            surface,
            Color("red"),
            (100, 100),
            (50, 20),
            False,
            12,
        )
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
