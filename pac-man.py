import logging

import pygame
from pygame.time import Clock
from pygame import Color, Vector2

from src.visual import Context
from src.visual.scenes.game_scene import VisualMaze
from src.visual.ui.button import Button
from src.visual.ui.prompt import Prompt

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font("assets/perfect_dos_vga_437.ttf", 16)

    WIDTH, HEIGHT = 960, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    clock = Clock()

    context = Context(screen, WIDTH, HEIGHT, font)
    scr = VisualMaze(context)
    content = font.render("Press!", False, Color("white"))
    button = Button(
        context,
        content,
        Vector2(64, 32),
        Color("crimson"),
        lambda: exit(),
    )
    button.local_position = Vector2(670, 200)
    button1 = Button(
        context,
        "You?",
        Vector2(64, 32),
        Color("teal"),
        lambda: None,
    )
    button1.local_position = Vector2(680, 200)
    button.add_child(button1)
    button2 = Button(
        context,
        "You?",
        Vector2(64, 32),
        Color("yellow"),
        lambda: None,
    )
    button2.local_position = Vector2(690, 200)
    button.add_child(button2)
    prompt = Prompt(context, "bruh", "hello world?" * 5, True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_q
            ):
                pygame.quit()
                return

            scr.handle_input(event)
            button.handle_input(event)
            button1.handle_input(event)
            prompt.handle_input(event)

        screen.fill(Color("#000000"))
        delta = clock.tick() / 1000

        scr.update(delta)
        button.update(delta)
        button1.update(delta)

        scr.render()
        button.render()
        button1.render()
        prompt.render()

        pygame.display.flip()


if __name__ == "__main__":
    main()
