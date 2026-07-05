import pygame
from pygame.time import Clock
from pygame import Color

from src.visual.screen import Screen


def main():
    pygame.init()
    pygame.font.init()
    WIDTH, HEIGHT = 960, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    clock = pygame.time.Clock()

    scr = Screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(Color("#000000"))
        delta = clock.tick() / 1000
        pygame.display.flip()


if __name__ == "__main__":
    main()
