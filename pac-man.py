import pygame
from pygame.time import Clock
from pygame import Color, Vector2

from src.visual.scenes.game_scene import VisualMaze
from src.visual.ui.button import Button


def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 16)

    WIDTH, HEIGHT = 960, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    clock = Clock()

    scr = VisualMaze()
    button = Button(lambda: exit(), Vector2(35, 20))
    button.local_position = Vector2(670, 200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            scr.handle_input(event)
            button.handle_input(event)

        screen.fill(Color("#000000"))
        delta = clock.tick() / 1000

        scr.update(delta)
        button.update(delta)

        scr.render(screen)
        button.render(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
