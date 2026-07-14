import pygame
from src.visual import Node, Context
from src.visual.scenes.game import GameScene
from src.visual.scenes.leaderboard import LeaderBoardScene
from src.visual.ui.button import Button
from src.visual.ui.label import Label
from pygame import Color, Vector2


class TitleScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        button_size = Vector2(120, 48)
        title_text = Label(
            context,
            Vector2(300, 200),
            [("Pac", Color("red")), ("Man", Color("blue"))],
            4,
        )

        def start_game():
            context.root_scene.remove_child(self)
            context.root_scene.add_child(GameScene(context))

        start_button = Button(
            context, "Start", button_size, Color("cyan"), start_game
        )

        def open_leader_board():
            context.root_scene.add_child(LeaderBoardScene(context))

        leaderboard_button = Button(
            context,
            "LeaderBoard",
            button_size,
            Color("gold"),
            open_leader_board,
        )

        def quit_game():
            context.game_running = False

        exit_button = Button(
            context, "Quit", button_size, Color("red"), quit_game
        )

        width, height = context.width, context.height
        title_text.local_position = (
            Vector2(width / 2, height / 5) - title_text.size / 2
        )
        start_button.local_position = (
            Vector2(width / 2, height * 2 / 5) - start_button.size / 2
        )
        leaderboard_button.local_position = (
            Vector2(width / 2, height * 3 / 5) - leaderboard_button.size / 2
        )
        exit_button.local_position = (
            Vector2(width / 2, height * 4 / 5) - exit_button.size / 2
        )

        self.add_child(title_text)
        self.add_child(start_button)
        self.add_child(leaderboard_button)
        self.add_child(exit_button)
