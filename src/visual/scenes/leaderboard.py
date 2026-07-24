from src.visual import Node, Context
from src.visual.ui.label import Label
from src.visual.ui.panel import Panel
from pygame import Color, Vector2, MOUSEBUTTONDOWN
from pygame.event import Event


class LeaderBoardScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        width, height = context.width, context.height
        panel = Panel(
            context,
            Vector2(300, 450),
            Color("darkgray"),
            on_outside_press=lambda x: self.free_from_scene(),
        )
        panel.local_position = Vector2(
            width / 2 - panel.size.x / 2, height / 7
        )
        self.add_child(panel)

        title_text = Label(
            context,
            Vector2(300, 200),
            [("LeaderBoard", Color("white"))],
            2,
        )
        title_text.local_position = (
            Vector2(width / 2, height / 5) - title_text.size / 2
        )
        self.add_child(title_text)

        self.entries = []
        for i, user in enumerate(context.user_manager.get_leaderboard()[:10]):
            entry = Label(
                context,
                Vector2(panel.size.x, panel.size.y / 12),
                [
                    (f"{user.username}:    ", Color("white")),
                    (str(user.highscore), Color("gold")),
                ],
            )
            entry.local_position = Vector2(0, (panel.size.y * (i + 2)) / 13)
            self.entries.append(entry)
            panel.add_child(entry)

    def _on_input(self, event: Event) -> Event | None:
        if event.type == MOUSEBUTTONDOWN:
            self.context.root_scene.remove_child(self)
