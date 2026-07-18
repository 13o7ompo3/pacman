from enum import Enum
from pygame import Color, Vector2
from src.visual import Node, Context
from src.visual.ui.label import Label
from src.visual.ui.panel import Panel
from src.visual.ui.text_box import TextBox
from src.visual.ui.prompt import Prompt
from typing import Callable


class LoginStep(Enum):
    USERNAME = "username"
    PASSWORD = "password"


class InputForm(Node):
    def __init__(
        self,
        context: "Context",
        label_text: str,
        is_password: bool,
        on_submit: Callable,
    ) -> None:
        super().__init__(context)

        label = Label(
            context,
            Vector2(300, 200),
            [
                (label_text, Color("white")),
            ],
        )
        label.local_position = (
            Vector2(context.width / 2, context.height * 4 / 8) - label.size / 2
        )

        self.text_box = TextBox(context, 24, on_submit, is_password)
        self.text_box.local_position = (
            Vector2(context.width / 2, context.height * 5 / 8)
            - self.text_box.size / 2
        )
        self.add_child(label)
        self.add_child(self.text_box)

    @property
    def value(self) -> str:
        return self.text_box.content


class GameOverScene(Node):
    def __init__(self, context: Context, final_score: int) -> None:
        super().__init__(context)
        self.login_step = LoginStep.USERNAME
        panel = Panel(
            context,
            Vector2(300, 450),
            Color("darkgray"),
            on_outside_press=lambda x: None,
        )
        panel.local_position = Vector2(
            context.width / 2 - panel.size.x / 2, context.height / 7
        )

        title = Label(
            context,
            Vector2(300, 200),
            [("Game Over", Color("orange"))],
            2,
        )
        title.local_position = (
            Vector2(context.width / 2, context.height / 4) - title.size / 2
        )

        score = Label(
            context,
            Vector2(300, 200),
            [
                ("Final Score: ", Color("white")),
                (str(final_score), Color("gold")),
            ],
        )
        score.local_position = (
            Vector2(context.width / 2, context.height * 3 / 8) - score.size / 2
        )

        self.username: str = ""
        user_manager = self.context.user_manager

        username_form: InputForm
        password_form: InputForm

        def on_username_submit(_):
            username_form.hidden = True
            password_form.hidden = False

        def on_password_submit(_):
            try:
                if user_manager.is_existing_user(username_form.value):
                    user_manager.authenticate_user(
                        username_form.value, password_form.value
                    )
                else:
                    user_manager.create_new_user(
                        username_form.value, password_form.value
                    )
                user_manager.update_highscore(final_score)

                from src.visual.scenes.title import TitleScene

                def go_to_title(_):
                    context.root_scene.clear_children()
                    context.root_scene.add_child(TitleScene(context))

                self.add_child(
                    Prompt(
                        context,
                        "Success",
                        f"Updated score for {username_form.value}",
                        go_to_title,
                    )
                )
            except Exception as error:
                print(error)

                self.add_child(
                    Prompt(context, "Error", str(error), lambda x: None)
                )
                username_form.hidden = False
                password_form.hidden = True
                username_form.text_box.content = ""
                password_form.text_box.content = ""

        username_form = InputForm(
            context, "Username: ", False, on_username_submit
        )
        password_form = InputForm(
            context, "Password: ", False, on_password_submit
        )
        password_form.hidden = True

        self.add_child(panel)
        self.add_child(title)
        self.add_child(score)
        self.add_child(password_form)
        self.add_child(username_form)
