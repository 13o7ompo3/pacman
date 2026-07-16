from src.visual import GameComponent, Node, Context
from src.visual.ui.button import Button
from src.visual.ui.label import Label
from pygame import Color, Rect, Vector2, MOUSEBUTTONDOWN, draw
from src.visual.ui.panel import Panel


class PauseScene(Node):
    def __init__(
        self, context: Context, scene_to_pause: GameComponent
    ) -> None:
        from src.visual.scenes.title import TitleScene

        super().__init__(context)

        width, height = context.width, context.height

        def resume_game(_):
            self.free_from_scene()
            scene_to_pause.paused = False

        panel = Panel(
            context,
            Vector2(300, 450),
            Color("darkgray"),
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
            [("Pause", Color("white"))],
            2,
        )

        resume_button = Button(
            context, "Resume", Vector2(150, 30), Color("green"), resume_game
        )

        def go_to_title(_):
            context.root_scene.clear_children()
            context.root_scene.add_child(TitleScene(context))

        title_button = Button(
            context,
            "Quit To Tittle",
            Vector2(150, 30),
            Color("red"),
            go_to_title,
        )

        width, height = context.width, context.height
        title_text.local_position = (
            Vector2(width / 2, height / 4) - title_text.size / 2
        )
        resume_button.local_position = (
            Vector2(width / 2, height * 2 / 4) - resume_button.size / 2
        )
        title_button.local_position = (
            Vector2(width / 2, height * 3 / 4) - title_button.size / 2
        )

        self.add_child(panel)
        self.add_child(title_text)
        self.add_child(resume_button)
        self.add_child(title_button)

    def _on_draw(self) -> None:
        draw.rect(
            self.context.screen,
            Color("black"),
            Rect((0, 0), (self.context.width, self.context.width)),
        )
