from pygame import Color, Vector2
from pygame.event import Event
from src.visual import Node, Context
from src.visual.ui.button import Button
from src.visual.ui.label import Label
from src.visual.utils.sprite import Sprite


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

        sp = Sprite(
            context,
            context.assets.image("movements_instruction"),
            1,
            8,
            2,
            True,
        )
        sp.local_position = Vector2(context.width, context.height) / 2
        breaking = Label(
            context,
            Vector2(100, 0),
            [(" BREAKING ", context.colors.light)],
            background_color=context.colors.dark,
            scale=2,
        )
        breaking.local_position.y = (
            context.height - breaking.size.y - next_button.size.y - 20
        )
        self.text = Label(
            context,
            Vector2(1400, breaking.size.y),
            [
                (
                    "To move around you can use arrow keys. vim motions are also supported alongside WASD.",
                    context.colors.lightest,
                )
            ],
            background_color=context.colors.darkest,
        )
        self.text.local_position = breaking.local_position + Vector2(
            breaking.size.x, 0
        )
        self.add_child(next_button)
        self.add_child(previous_button)
        self.add_child(return_button)
        self.add_child(sp)
        self.add_child(self.text)
        self.add_child(breaking)

    def _on_update(self, delta: float) -> None:
        self.text.local_position.x -= 100 * delta
        if -self.text.local_position.x > self.text.size.x / 2:
            self.text.local_position.x = 0

    def _on_input(self, event: Event) -> Event | None:
        return

    def _on_draw(self) -> None:
        self.context.screen.fill(self.context.colors.darker)
