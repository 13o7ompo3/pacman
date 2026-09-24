"""The title scene of the game."""

import pygame

from src.visual import Context, Node
from src.visual.scenes.game import GameScene
from src.visual.scenes.instructions import InstructionsScene
from src.visual.scenes.leaderboard import LeaderBoardScene
from src.visual.ui.button import Button
from src.visual.utils.primitives import Vec2


class TitleScene(Node):
    """A class that represents the title scene.

    Attributes:
        context (Context): The context of the game.

    """

    def __init__(self, context: Context) -> None:
        """Initialize a TitleScene instance.

        Args:
            context (Context): The context of the game.
        """
        super().__init__(context)
        context.root_scene.parallax_background.velocity = 60
        button_size = Vec2(130, 38)
        self.title_text = context.assets.image("banner")

        def start_game(button: Button) -> None:
            """Start the game by removing the title scene.

            Args:
                button (Button): The button that was pressed.
            """
            context.root_scene.remove_child(self)
            context.root_scene.add_child(GameScene(context))

        start_button = Button(
            context,
            [context.assets.image("play_icon"), "Start".center(12)],
            button_size,
            context.colors.light,
            start_game,
            shortcuts={pygame.K_SPACE, pygame.K_RETURN},
            shadow_color=context.colors.dark,
        )

        def open_leader_board(button: Button) -> None:
            """Open the leaderboard scene by removing the title scene.

            Args:
                button (Button): The button that was pressed.
            """
            context.root_scene.add_child(LeaderBoardScene(context))

        leaderboard_button = Button(
            context,
            [context.assets.image("cup_icon"), "LeaderBoard".center(12)],
            button_size,
            context.colors.light,
            open_leader_board,
            shadow_color=context.colors.dark,
            shortcuts={pygame.K_l},
        )

        def open_instructions(button: Button) -> None:
            """Open the instructions scene by removing the title scene.

            Args:
                button (Button): The button that was pressed.
            """
            instruction_scene = InstructionsScene(context)
            context.root_scene.add_child(instruction_scene)

        instructions_button = Button(
            context,
            [
                context.assets.image("instructions_icon"),
                "Instructions".center(12),
            ],
            button_size,
            context.colors.light,
            open_instructions,
            shadow_color=context.colors.dark,
            shortcuts={pygame.K_i},
        )

        def quit_game(button: Button) -> None:
            """Quit the game by setting the game_running flag to False.

            Args:
                button (Button): The button that was pressed.
            """
            context.game_running = False

        exit_button = Button(
            context,
            [context.assets.image("exit_icon"), "Quit".center(12)],
            button_size,
            context.colors.dark,
            quit_game,
            shadow_color=context.colors.darker,
            shortcuts={pygame.K_ESCAPE, pygame.K_q},
        )

        theme_button = Button(
            context,
            context.assets.image("theme_icon"),
            Vec2(32, 32),
            context.colors.light,
            lambda _: context.root_scene.change_theme(),
            shadow_color=context.colors.dark,
        )

        width, height = context.width, context.height
        start_button.local_position = (
            Vec2(width / 2, height * 2 / 6) - start_button.size / 2
        )
        leaderboard_button.local_position = (
            Vec2(width / 2, height * 3 / 6) - leaderboard_button.size / 2
        )
        instructions_button.local_position = (
            Vec2(width / 2, height * 4 / 6) - exit_button.size / 2
        )
        exit_button.local_position = (
            Vec2(width / 2, height * 5 / 6) - exit_button.size / 2
        )
        theme_button.local_position = (
            Vec2(width, height) - theme_button.size - Vec2(10, 10)
        )

        self.add_child(start_button)
        self.add_child(leaderboard_button)
        self.add_child(instructions_button)
        self.add_child(exit_button)
        self.add_child(theme_button)

    def _on_draw(self) -> None:
        """Draw the title scene."""
        self.context.screen.blit(
            self.title_text,
            (
                Vec2(self.context.width / 2, self.context.height / 6)
                - Vec2(self.title_text.get_size()) / 2
            ).as_tuple(),
        )
