from src.visual import Node, Context
from src.visual.ui.label import Label
from pygame import Color, Vector2, MOUSEBUTTONDOWN
from pygame.event import Event


class LeaderBoardScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        title_text = Label(
            context,
            Vector2(300, 200),
            [("LeaderBoard", Color("white"))],
            2,
        )

        width, height = context.width, context.height
        title_text.local_position = (
            Vector2(width / 2, height / 5) - title_text.size / 2
        )

        self.add_child(title_text)

    def _on_input(self, event: Event) -> Event | None:
        if event.type == MOUSEBUTTONDOWN:
            self.context.root_scene.remove_child(self)
