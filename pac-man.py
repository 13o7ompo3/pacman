import logging

from src.visual.utils.asset_manager import AssetError


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def main() -> None:
    """Main function to run the game."""
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
    from src.parser import parse_config

    pygame.init()
    pygame.font.init()

    WIDTH, HEIGHT = 640, 480
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

    pygame.display.set_icon(AssetManager.load_image("assets/icons/icon.png"))

    user_manager = UserManager()

    assets = AssetManager()
    config = parse_config("config.json")

    context = Context(surface, WIDTH, HEIGHT, assets, user_manager, config)
    loading_scene = LoadingScene(context)
    context.root_scene.add_child(loading_scene)

    clock = Clock()
    while context.game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
    try:
        main()
    except AssetError as err:
        logging.error(str(err))
    except KeyboardInterrupt:
        logging.warning("Program stopped by the user..")
    except Exception as err:
        logging.error(f"Error: {err}")
