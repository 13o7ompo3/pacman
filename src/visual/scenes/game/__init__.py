from parser import LevelConfig
from src.visual import Node, Context
from src.logical.maze import Direction, LogicalMaze
from src.visual.scenes.game.maze import VisualMaze
from src.visual.draw import Draw
from src.visual.ui.progress import ProgressBar, ProgressBarOrientation
from src.visual.ui.label import Label
from pygame import Color, Vector2, draw
from pygame import image, Surface
import math

from src.visual.ui.button import Button
from src.visual.scenes.pause import PauseScene


class GumTimer(Node):
    def __init__(
        self, context: Context, logical_maze: LogicalMaze, radius: int
    ) -> None:
        super().__init__(context)
        self.logical_maze = logical_maze
        self.radius = radius
        self.label = Label(
            context,
            Vector2(100, 20),
            [("SUPER PACGUM", Color("cyan"))],
        )
        self.add_child(self.label)

    def _on_draw(self) -> None:
        Draw.sector(
            self.context.screen,
            Color("blue"),
            self.world_position
            + self.label.size / 2
            + Vector2(0, self.radius * 1.5),
            0,
            self.radius - 1,
            0,
            2
            * math.pi
            * self.logical_maze.player.gum_timer
            / self.logical_maze.super_pacgum_duration,
            True,
        )
        Draw.circle(
            self.context.screen,
            self.world_position
            + self.label.size / 2
            + Vector2(0, self.radius * 1.5),
            self.radius,
            border_color=Color("white"),
            border_width=2,
        )


class TitleLabel(Node):
    def __init__(
        self,
        context: Context,
        static_text: str,
        dynamic_text: str,
        width: int,
        accent_color: Color,
    ) -> None:
        super().__init__(context)
        self.static_text = static_text
        self.dynamic_text = dynamic_text
        self.width = width
        self.line_thickness = 4
        self.accent_color = accent_color
        self.label = Label(
            self.context,
            Vector2(),
            [
                (self.static_text, Color("white")),
                (self.dynamic_text, self.accent_color),
            ],
        )

    def update_dynamic_text(self, val: str) -> None:
        if self.dynamic_text != val:
            self.label = Label(
                self.context,
                Vector2(),
                [
                    (self.static_text, Color("white")),
                    (self.dynamic_text, self.accent_color),
                ],
            )
            self.dynamic_text = val

    def _on_draw(self) -> None:
        Draw.rect(
            self.context.screen,
            self.world_position
            + Vector2(0, self.label.size.y / 2 - self.line_thickness / 2),
            Vector2(
                self.width / 2 - self.label.size.x * 1.2 / 2,
                self.line_thickness,
            ),
            fill_color=Color("cyan"),
        )
        Draw.rect(
            self.context.screen,
            self.world_position
            + Vector2(
                self.width / 2 + self.label.size.x * 1.2 / 2,
                self.label.size.y / 2 - self.line_thickness / 2,
            ),
            Vector2(
                self.width / 2 - self.label.size.x * 1.2 / 2,
                self.line_thickness,
            ),
            fill_color=Color("cyan"),
        )
        self.label.local_position = self.world_position + Vector2(
            self.width / 2 - self.label.size.x / 2, 0
        )
        self.label.render()


class InfoBar(Node):
    def __init__(
        self,
        context: Context,
        static_text: str,
        dynamic_text: str,
        icon: Surface,
        width: int,
        max_progress: int,
        reversed: bool,
        progress_color: Color,
    ) -> None:
        super().__init__(context)
        self.width = width
        self.icon = icon

        self.dynamic_text = dynamic_text
        self.static_text = static_text

        self.static_label = self.context.assets.font("ui").render(
            static_text.center(8), False, Color("white")
        )
        self.dynamic_label = self.context.assets.font("ui").render(
            dynamic_text.center(8), False, Color("white")
        )
        self.max_progress = max_progress

        self.last_world_pos = self.world_position
        self.progress = ProgressBar(
            self.context,
            Vector2(
                width
                - self.dynamic_label.get_size()[0] * 1.2
                - self.icon.get_size()[0] * 1.2,
                16,
            ),
            ProgressBarOrientation.HORIZONTAL,
            progress_color=progress_color,
            border_radius=0,
            total=max_progress,
        )
        self.reversed = reversed

        self._update_positions()
        self.add_child(self.progress)

    def update_dynamic_text(self, val: int) -> None:
        if reversed:
            val = self.max_progress - val
        if self.dynamic_text != str(val):
            self.dynamic_text = str(val)
            self.dynamic_label = self.context.assets.font("ui").render(
                self.dynamic_text.center(8), False, Color("white")
            )
            self.progress.progress = val

    def _update_positions(self) -> None:
        self.icon_pos = self.world_position + Vector2(
            0,
            self.static_label.get_size()[1] * 1.2
            - self.dynamic_label.get_size()[1] / 2,
        )
        self.static_text_pos = self.world_position + Vector2(
            self.width / 2 - self.static_label.get_size()[0] / 2, 0
        )
        self.dynamic_text_pos = self.world_position + Vector2(
            self.width - self.dynamic_label.get_size()[0],
            self.static_label.get_size()[1] * 1.2,
        )
        self.progress.local_position = Vector2(
            self.icon.get_size()[0] * 1.6,
            self.static_label.get_size()[1] * 1.2,
        )

    def _on_update(self, delta: float) -> None:
        if self.last_world_pos != self.world_position:
            self._update_positions()
            self.last_world_pos = self.world_position

    def _on_draw(self) -> None:
        self.context.screen.blit(
            self.static_label,
            self.static_text_pos,
        )
        self.context.screen.blit(
            self.icon,
            self.icon_pos,
        )
        self.context.screen.blit(
            self.dynamic_label,
            self.dynamic_text_pos,
        )


class LivesLeft(Node):
    def __init__(self, context: "Context", logical_maze: LogicalMaze) -> None:
        super().__init__(context)

        self.logical_maze = logical_maze
        self.last_level = self.logical_maze.current_level_idx
        self.life_img = image.load("./assets/icons/life.png")

        self.lives_text = self.context.assets.font("ui").render(
            "Lives remaining: ", False, Color("white")
        )

    def _on_draw(self) -> None:
        self.context.screen.blit(
            self.lives_text,
            self.world_position,
        )
        for i in range(self.logical_maze.player.lives):
            self.context.screen.blit(
                self.life_img, self.world_position + (32 * i + 20, 30)
            )


class GameScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        levels = [
            LevelConfig(width=15, height=15, seed=1337),
            # LevelConfig(width=10, height=13, seed=42),
        ]
        max_ticks = 4000
        self.logical_maze = LogicalMaze(levels, max_ticks=max_ticks)
        self.maze = VisualMaze(context, self.logical_maze)
        self.maze = self.maze
        self.maze.local_position = (
            Vector2(context.width, context.height) / 2 - self.maze.size / 2
        )

        pause_button = Button(
            context,
            "=",
            Vector2(30, 30),
            Color("white"),
            lambda _: context.root_scene.add_child(
                PauseScene(context, self.maze)
            ),
        )
        gum_timer = GumTimer(context, self.logical_maze, 32)
        gum_timer.local_position = self.maze.local_position + Vector2(-200, 50)

        lives_left = LivesLeft(context, self.logical_maze)
        lives_left.local_position = self.maze.local_position + Vector2(
            -210, self.maze.size.y - 150
        )

        self.score_title_label = TitleLabel(
            context,
            "SCORE: ",
            str(self.logical_maze.player.score),
            int(self.maze.size.x),
            Color("red"),
        )
        self.score_title_label.local_position = (
            self.maze.world_position - Vector2(0, 50)
        )

        self.level_title_label = TitleLabel(
            context,
            "LEVEL: ",
            str(self.logical_maze.current_level_idx + 1),
            int(self.maze.size.x),
            Color("yellow"),
        )
        self.level_title_label.local_position = (
            self.maze.world_position + Vector2(0, self.maze.size.y + 40)
        )

        self.time_bar = InfoBar(
            context,
            "TIME LEFT",
            "0",
            image.load("./assets/icons/clock.png"),
            int(context.width / 2 - self.maze.size.x / 2),
            int(self.logical_maze.ticks_remaining / 60),
            False,
            Color("orange"),
        )
        self.time_bar.local_position = self.maze.local_position + Vector2(
            self.maze.size.x + 10, self.maze.size.y / 2 - 76
        )

        self.gums_bar = InfoBar(
            context,
            "GUMS EATEN",
            "43/200",
            image.load("./assets/icons/gum.png"),
            int(context.width / 2 - self.maze.size.x / 2),
            len(self.logical_maze.pacgums),
            True,
            Color("blue"),
        )
        self.gums_bar.local_position = self.maze.local_position + Vector2(
            self.maze.size.x + 10, self.maze.size.y / 2 + 50
        )

        self.add_child(self.maze)
        self.add_child(self.score_title_label)
        self.add_child(self.level_title_label)
        self.add_child(self.time_bar)
        self.add_child(self.gums_bar)
        self.add_child(gum_timer)
        self.add_child(lives_left)
        self.add_child(pause_button)

    def _on_update(self, delta: float) -> None:
        self.score_title_label.update_dynamic_text(
            str(self.logical_maze.player.score)
        )
        self.level_title_label.update_dynamic_text(
            str(self.logical_maze.current_level_idx + 1)
        )
        self.gums_bar.update_dynamic_text(len(self.logical_maze.pacgums))
        self.time_bar.update_dynamic_text(
            int(self.logical_maze.ticks_remaining / 60)
        )
