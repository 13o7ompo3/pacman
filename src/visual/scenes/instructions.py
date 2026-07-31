from pygame import Color, Vector2
from pygame.event import Event
from src.visual import Node, Context
from src.visual.ui.button import Button


class InstructionsScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)

        def go_next(_):
            pass

        next_button = Button(
            context,
            ["Next".center(8), context.assets.image("next_icon")],
            Vector2(50, 25),
            context.colors.light,
            go_next,
            shadow_color=context.colors.dark,
        )
        next_button.local_position = (
            Vector2(context.width - 10, context.height - 10) - next_button.size
        )

        def go_prev(_):
            pass

        previous_button = Button(
            context,
            [context.assets.image("previous_icon"), "Previous".center(8)],
            Vector2(50, 25),
            context.colors.light,
            go_prev,
            shadow_color=context.colors.dark,
        )
        previous_button.local_position = Vector2(
            10, context.height - previous_button.size.y - 10
        )

        def go_back(_):
            self.free_from_scene()

        return_button = Button(
            context,
            [context.assets.image("return_icon"), "Back".center(8)],
            Vector2(50, 25),
            context.colors.dark,
            go_back,
            shadow_color=context.colors.darker,
        )
        return_button.local_position = Vector2(10, 10)

        self.add_child(next_button)
        self.add_child(previous_button)
        self.add_child(return_button)

    def _on_input(self, event: Event) -> Event | None:
        return

    def _on_draw(self) -> None:
        self.context.screen.fill(self.context.colors.darkest)
