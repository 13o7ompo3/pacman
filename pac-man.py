import pygame
from pygame.time import Clock
from pygame import Color, Vector2

from src.visual.scene import Scene


def main():
    pygame.init()
    # pygame.font.init()
    WIDTH, HEIGHT = 960, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    clock = pygame.time.Clock()

    scr = Scene()

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


if __name__ == "__main__":
    main()
