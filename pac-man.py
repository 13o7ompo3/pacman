<<<<<<< HEAD
import pygame
from pygame.time import Clock
from pygame import Color, Vector2

from src.visual.scenes.game_scene import VisualMaze
=======
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
from src.visual.ui.label import Label
from src.visual.ui.panel import Panel
from src.visual.ui.progress import ProgressBar, ProgressBarOrientation
from src.visual.ui.text_box import TextBox

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
>>>>>>> main


def main():
    pygame.init()
<<<<<<< HEAD
    # pygame.font.init()
    WIDTH, HEIGHT = 960, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    clock = Clock()

    scr = VisualMaze()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            scr.handle_input(event)

        screen.fill(Color("#000000"))
        delta = clock.tick() / 1000

        scr.update(delta)
        scr.render(screen)
        pygame.display.flip()

=======
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

        pygame.display.flip()

    pygame.quit()

>>>>>>> main

if __name__ == "__main__":
    main()
