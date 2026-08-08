import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():
    import os

    # hide pygame hello message
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
    import pygame
    from pygame.time import Clock
    from src.visual.draw import Draw

    from src.db_manager.user import UserManager
    from src.visual import Context
    from src.visual.scenes.loading import LoadingScene
    from src.visual.utils.asset_manager import AssetManager
    from parser import parse_config

    pygame.init()
    pygame.font.init()

    WIDTH, HEIGHT = 640, 480
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

    user_manager = UserManager()

    assets = AssetManager()
    config = parse_config("config.json")

    context = Context(surface, WIDTH, HEIGHT, assets, user_manager, config)
    loading_scene = LoadingScene(context)
    context.root_scene.add_child(loading_scene)

    clock = Clock()
    while context.game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and event.key in {pygame.K_ESCAPE, pygame.K_q}
            ):
                context.game_running = False

            # send input events to the node tree
            context.root_scene.handle_input(event)

        # update the scene tree
        delta = clock.tick() / 1000
        context.root_scene.update(delta)

        # clear the background
        Draw.rect(surface, (0, 0), (WIDTH, HEIGHT), context.colors.darkest)

        # render the scene tree
        context.root_scene.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
