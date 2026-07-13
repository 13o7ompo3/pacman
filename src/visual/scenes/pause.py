from src.visual import GameComponent, Node, Context
from src.visual.ui.button import Button
from src.visual.ui.label import Label
from pygame import Color, Vector2, MOUSEBUTTONDOWN
from pygame.event import Event


class PauseScene(Node):
    def __init__(
        self, context: Context, scene_to_pause: GameComponent
    ) -> None:
        from src.visual.scenes.title import TitleScene

        super().__init__(context)
        scene_to_pause.paused = True

        title_text = Label(
            context,
            Vector2(300, 200),
            [("Pause", Color("white"))],
            2,
        )

        def resume_game():
            context.root_scene.remove_child(self)
            scene_to_pause.paused = False

        resume_button = Button(
            context, "Resume", Vector2(70, 30), Color("green"), resume_game
        )

        def go_to_title():
            context.root_scene.clear_children()
            context.root_scene.add_child(TitleScene(context))

        title_button = Button(
            context,
            "Quit To Tittle",
            Vector2(70, 30),
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

        self.add_child(title_text)
        self.add_child(resume_button)
        self.add_child(title_button)

    def _on_input(self, event: Event) -> Event | None:
        if event.type == MOUSEBUTTONDOWN:
            self.context.root_scene.remove_child(self)
