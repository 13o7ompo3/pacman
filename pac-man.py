import logging

import pygame
from pygame.time import Clock
from pygame import Color

from src.visual import Context, GameComponent, Node
from src.visual.scenes.game import VisualMaze
from src.visual.scenes.title import TitleScene

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font("assets/perfect_dos_vga_437.ttf", 16)

    WIDTH, HEIGHT = 960, 600
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

    context = Context(surface, WIDTH, HEIGHT, font)
    title_scene = TitleScene(context)
    context.root_scene.add_child(title_scene)

    clock = Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and event.key in {pygame.K_ESCAPE, pygame.K_q}
            ):
                pygame.quit()
                return

            context.root_scene.handle_input(event)

        surface.fill(Color("black"))
        delta = clock.tick() / 1000

        context.root_scene.update(delta)

        context.root_scene.render()

        pygame.display.flip()


if __name__ == "__main__":
    main()
