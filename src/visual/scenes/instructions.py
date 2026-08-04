from pygame import Color, Vector2
from pygame.event import Event
from src.visual import Node, Context
from src.visual.draw import Draw
from src.visual.ui.button import Button
from src.visual.ui.label import Label
from src.visual.utils.sprite import Sprite
from typing import Any


class InstructionPage(Node):
    def __init__(
        self, context: Context, sprite: Sprite, heading: str, description: str
    ) -> None:
        super().__init__(context)

        self.sprite = sprite
        title_text = Label(
            context,
            Vector2(0, 0),
            [(f" {heading} ", context.colors.light)],
            background_color=context.colors.dark,
            scale=2,
            border_color=context.colors.lightest,
            border_radius=8,
        )
        title_text.local_position = Vector2(
            context.width / 2 - title_text.size.x / 2, 50
        )
        sprite.local_position = Vector2(context.width, context.height) / 2
        self.breaking_text = Label(
            context,
            Vector2(100, 0),
            [(" BREAKING ", context.colors.light)],
            background_color=context.colors.dark,
            scale=2,
        )
        self.breaking_text.local_position.y = (
            context.height - self.breaking_text.size.y - 45
        )
        self.text = Label(
            context,
            Vector2(0, self.breaking_text.size.y),
            [
                (
                    description,
                    context.colors.lightest,
                )
            ],
        )
        self.text.local_position = self.breaking_text.local_position + Vector2(
            self.breaking_text.size.x, 0
        )

        self.add_child(title_text)
        self.add_child(sprite)
        self.add_child(self.text)
        self.add_child(self.breaking_text)

    def __setattr__(self, name: str, value: Any, /) -> None:
        ret = super().__setattr__(name, value)
        if name == "hidden" and hasattr(self, "sprite"):
            if not self.hidden:
                self.sprite.current_frame_index = 0
        return ret

    def _on_update(self, delta: float) -> None:
        self.text.local_position.x -= 100 * delta
        if (
            -self.text.local_position.x + self.breaking_text.size.x
            > self.text.size.x
        ):
            self.text.local_position.x = self.context.width

    def _on_draw(self) -> None:
        Draw.rect(
            self.context.screen,
            self.breaking_text.local_position,
            (self.context.width, int(self.breaking_text.size.y)),
            fill_color=self.context.colors.darkest,
        )


class InstructionsScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)

        self.pages = [
            InstructionPage(
                context,
                Sprite(
                    context,
                    context.assets.image("movements_instruction"),
                    1,
                    8,
                    2,
                    True,
                ),
                "Movements",
                "To move around you can use arrow keys. vim motions are also supported alongside WASD.",
            ),
            InstructionPage(
                context,
                Sprite(
                    context,
                    context.assets.image("losing_instruction"),
                    1,
                    2,
                    2,
                    True,
                ),
                "Losing",
                "In order to lose you must be an absolute loser.",
            ),
            InstructionPage(
                context,
                Sprite(
                    context,
                    context.assets.image("super_pacgum_instruction"),
                    1,
                    8,
                    2,
                    True,
                ),
                "Super Pacgum",
                "When you eat a super pacgum, the ghosts become edible for a short time and they run away from you on sight.",
            ),
            InstructionPage(
                context,
                Sprite(
                    context,
                    context.assets.image("winning_instruction"),
                    1,
                    16,
                    2,
                    True,
                ),
                "Winning",
                "To win the game you must win the game in order to win.",
            ),
        ]

        for page in self.pages:
            self.add_child(page)
            page.hidden = True

        self.current_page_idx = 0
        self.pages[self.current_page_idx].hidden = False

        def go_next(_):
            self.pages[self.current_page_idx].hidden = True
            if self.current_page_idx < len(self.pages) - 1:
                self.current_page_idx += 1
            self.pages[self.current_page_idx].hidden = False

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
            self.pages[self.current_page_idx].hidden = True
            if self.current_page_idx > 0:
                self.current_page_idx -= 1
            self.pages[self.current_page_idx].hidden = False

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
        self.context.screen.fill(self.context.colors.darker)
