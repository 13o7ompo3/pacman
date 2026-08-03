"""The pause scene module."""

from src.visual import GameComponent, Node, Context
from src.visual.ui.button import Button
from src.visual.ui.label import Label
from pygame import Vector2
from src.visual.ui.panel import Panel


class PauseScene(Node):
    """A class that represents the pause scene.

    Attributes:
        scene_to_pause (GameComponent): The game component to pause.

    """

    def __init__(
        self, context: Context, scene_to_pause: GameComponent
    ) -> None:
        """Initialize a PauseScene instance."""
        from src.visual.scenes.title import TitleScene

        super().__init__(context)

        width, height = context.width, context.height

        def resume_game(_):
            """Resume the game by removing the pause scene."""
            self.free_from_scene()
            scene_to_pause.paused = False

        panel = Panel(
            context,
            Vector2(300, 300),
            context.colors.darker,
            border_color=context.colors.darkest,
            on_outside_press=resume_game,
        )
        panel.local_position = Vector2(
            width / 2 - panel.size.x / 2, height / 7
        )

        self.scene_to_pause = scene_to_pause
        scene_to_pause.paused = True

        title_text = Label(
            context,
            Vector2(300, 200),
            [("Pause", context.colors.lightest)],
            2,
        )

        resume_button = Button(
            context,
            [context.assets.image("play_icon"), "Resume".center(14)],
            Vector2(150, 30),
            context.colors.light,
            resume_game,
            shadow_color=context.colors.dark,
        )

        def go_to_title(_):
            """Go to the title scene by clearing the root scene."""
            context.root_scene.clear_children()
            context.root_scene.add_child(TitleScene(context))

        title_button = Button(
            context,
            [context.assets.image("return_icon"), "Quit To Tittle".center(14)],
            Vector2(150, 30),
            context.colors.dark,
            go_to_title,
            shadow_color=context.colors.darker,
        )

        width, height = context.width, context.height
        title_text.local_position = (
            Vector2(width / 2, 50 + height * 1 / 6) - title_text.size / 2
        )
        resume_button.local_position = (
            Vector2(width / 2, 50 + height * 2 / 6) - resume_button.size / 2
        )
        title_button.local_position = (
            Vector2(width / 2, 50 + height * 3 / 6) - title_button.size / 2
        )

        self.add_child(panel)
        self.add_child(title_text)
        self.add_child(resume_button)
        self.add_child(title_button)
