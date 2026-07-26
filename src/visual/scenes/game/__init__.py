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
            2 * math.pi * 2000 / self.logical_maze.super_pacgum_duration,
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
        self.label = Label(
            context,
            Vector2(),
            [(static_text, Color("white")), (dynamic_text, accent_color)],
        )
        self.width = width
        self.line_thickness = 4

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
        static_label: str,
        dynamic_label: str,
        icon: Surface,
        width: int,
        max_progress: int,
        reversed: bool,
    ) -> None:
        super().__init__(context)
        self.width = width
        self.icon = icon

        self.static_text = context.font.render(
            static_label.center(8), False, Color("white")
        )
        self.dynamic_text = context.font.render(
            dynamic_label.center(8), False, Color("white")
        )

        self.last_world_pos = self.world_position
        self.progress = ProgressBar(
            self.context,
            Vector2(
                width
                - self.dynamic_text.get_size()[0] * 1.2
                - self.icon.get_size()[0] * 1.2,
                16,
            ),
            ProgressBarOrientation.HORIZONTAL,
            Color("blue"),
            border_radius=0,
            total=max_progress,
            reversed=reversed,
        )

        self._update_positions()
        self.add_child(self.progress)

    def _update_positions(self) -> None:
        self.icon_pos = self.world_position + Vector2(
            0,
            self.static_text.get_size()[1] * 1.2
            - self.dynamic_text.get_size()[1] / 2,
        )
        self.static_text_pos = self.world_position + Vector2(
            self.width / 2 - self.static_text.get_size()[0] / 2, 0
        )
        self.dynamic_text_pos = self.world_position + Vector2(
            self.width - self.dynamic_text.get_size()[0],
            self.static_text.get_size()[1] * 1.2,
        )
        self.progress.local_position = Vector2(
            self.icon.get_size()[0] * 1.6, self.static_text.get_size()[1] * 1.2
        )

    def _on_update(self, delta: float) -> None:
        if self.last_world_pos != self.world_position:
            self._update_positions()
            self.last_world_pos = self.world_position

    def _on_draw(self) -> None:
        self.context.screen.blit(
            self.static_text,
            self.static_text_pos,
        )
        self.context.screen.blit(
            self.icon,
            self.icon_pos,
        )
        self.context.screen.blit(
            self.dynamic_text,
            self.dynamic_text_pos,
        )


class LivesLeft(Node):
    def __init__(self, context: "Context", logical_maze: LogicalMaze) -> None:
        super().__init__(context)

        self.logical_maze = logical_maze
        self.last_level = self.logical_maze.current_level_idx
        self.life_img = image.load("./assets/icons/life.png")

        self.lives_text = self.context.font.render(
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
            LevelConfig(width=20, height=20, seed=1337),
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

        score_title_label = TitleLabel(
            context, "SCORE: ", "3435", int(self.maze.size.x), Color("red")
        )
        score_title_label.local_position = self.maze.world_position - Vector2(
            0, 50
        )

        level_title_label = TitleLabel(
            context, "LEVEL: ", "3", int(self.maze.size.x), Color("yellow")
        )
        level_title_label.local_position = self.maze.world_position + Vector2(
            0, self.maze.size.y + 40
        )

        time_bar = InfoBar(
            context,
            "TIME LEFT",
            "00:34",
            image.load("./assets/icons/clock.png"),
            int(context.width / 2 - self.maze.size.x / 2),
            100,
            True,
        )
        time_bar.local_position = self.maze.local_position + Vector2(
            self.maze.size.x + 10, self.maze.size.y / 2 - 76
        )

        gums_bar = InfoBar(
            context,
            "GUMS EATEN",
            "43",
            image.load("./assets/icons/gum.png"),
            int(context.width / 2 - self.maze.size.x / 2),
            100,
            False,
        )
        gums_bar.local_position = self.maze.local_position + Vector2(
            self.maze.size.x + 10, self.maze.size.y / 2 + 50
        )

        self.add_child(self.maze)
        self.add_child(score_title_label)
        self.add_child(level_title_label)
        self.add_child(time_bar)
        self.add_child(gums_bar)
        self.add_child(gum_timer)
        self.add_child(lives_left)
        self.add_child(pause_button)
