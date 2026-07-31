import pygame
from src.visual import Node, Context
from src.visual.scenes.game import GameScene
from src.visual.scenes.game_over import GameOverScene, TerminalState
from src.visual.scenes.leaderboard import LeaderBoardScene
from src.visual.scenes.instructions import InstructionsScene
from src.visual.ui.button import Button
from src.visual.ui.label import Label
from pygame import Color, Vector2


class TitleScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        button_size = Vector2(130, 38)
        title_text = Label(
            context,
            Vector2(300, 200),
            [("Pac", context.colors.dark), ("Man", context.colors.light)],
            4,
        )

        def start_game(_):
            context.root_scene.remove_child(self)
            context.root_scene.add_child(GameScene(context))

        start_button = Button(
            context,
            [context.assets.image("play_icon"), "Start".center(12)],
            button_size,
            context.colors.light,
            start_game,
            shortcuts={pygame.K_SPACE},
            shadow_color=context.colors.dark,
        )

        def open_leader_board(_):
            context.root_scene.add_child(LeaderBoardScene(context))

        leaderboard_button = Button(
            context,
            [context.assets.image("cup_icon"), "LeaderBoard".center(12)],
            button_size,
            context.colors.light,
            open_leader_board,
            shadow_color=context.colors.dark,
        )

        def open_instructions(_):
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
        )

        def quit_game(_):
            context.game_running = False

        exit_button = Button(
            context,
            [context.assets.image("exit_icon"), "Quit".center(12)],
            button_size,
            context.colors.dark,
            quit_game,
            shadow_color=context.colors.darker,
        )

        width, height = context.width, context.height
        title_text.local_position = (
            Vector2(width / 2, height / 6) - title_text.size / 2
        )
        start_button.local_position = (
            Vector2(width / 2, height * 2 / 6) - start_button.size / 2
        )
        leaderboard_button.local_position = (
            Vector2(width / 2, height * 3 / 6) - leaderboard_button.size / 2
        )
        instructions_button.local_position = (
            Vector2(width / 2, height * 4 / 6) - exit_button.size / 2
        )
        exit_button.local_position = (
            Vector2(width / 2, height * 5 / 6) - exit_button.size / 2
        )

        self.add_child(title_text)
        self.add_child(start_button)
        self.add_child(leaderboard_button)
        self.add_child(instructions_button)
        self.add_child(exit_button)
