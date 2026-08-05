"""A module that contains the GameScene class and related UI components."""

from src.logical.core_types import GhostState, PlayerState
from parser import LevelConfig
from src.visual import Node, Context
from src.logical.maze import LogicalMaze
from src.visual.scenes.game.maze import VisualMaze
from src.visual.draw import Draw
from src.visual.ui.progress import ProgressBar, ProgressBarOrientation
from src.visual.ui.label import Label
import pygame
from pygame import Color, Vector2
from pygame import Surface
from pygame.event import Event
import math

from src.visual.ui.button import Button
from src.visual.scenes.pause import PauseScene


class GumTimer(Node):
    """A class that represents a timer for the super pacgum effect.

    Attributes:
        logical_maze (LogicalMaze): The logical maze instance.
        radius (int): The radius of the timer circle.

    """

    def __init__(
        self, context: Context, logical_maze: LogicalMaze, radius: int
    ) -> None:
        """Initialize a GumTimer instance."""
        super().__init__(context)
        self.logical_maze = logical_maze
        self.radius = radius
        self.label = Label(
            context,
            Vector2(100, 20),
            [("SUPER PACGUM", context.colors.lightest)],
        )
        self.add_child(self.label)

    def _on_draw(self) -> None:
        """Draw the timer circle and label."""
        Draw.sector(
            self.context.screen,
            self.context.colors.dark,
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
            border_color=self.context.colors.lightest,
            border_width=2,
        )


class TitleLabel(Node):
    """A class that represents a title label with static and dynamic text.

    Attributes:
        static_text (str): The static text of the label.
        dynamic_text (str): The dynamic text of the label.
        width (int): The width of the label.
        line_thickness (int): The thickness of the lines.
        accent_color (Color): The color of the dynamic text.

    """

    def __init__(
        self,
        context: Context,
        static_text: str,
        dynamic_text: str,
        width: int,
        accent_color: Color,
    ) -> None:
        """Initialize a TitleLabel instance."""
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
                (self.static_text, context.colors.lightest),
                (self.dynamic_text, self.accent_color),
            ],
        )

    def update_dynamic_text(self, val: str) -> None:
        """Update the dynamic text of the label, recreate the label on change.

        Args:
            val (str): The new dynamic text value.

        """
        if self.dynamic_text != val:
            self.label = Label(
                self.context,
                Vector2(),
                [
                    (self.static_text, self.context.colors.lightest),
                    (self.dynamic_text, self.accent_color),
                ],
            )
            self.dynamic_text = val

    def _on_draw(self) -> None:
        """Draw the title label with lines and text."""
        Draw.rect(
            self.context.screen,
            self.world_position
            + Vector2(0, self.label.size.y / 2 - self.line_thickness / 2),
            Vector2(
                self.width / 2 - self.label.size.x * 1.2 / 2,
                self.line_thickness,
            ),
            fill_color=self.context.colors.light,
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
            fill_color=self.context.colors.light,
        )
        self.label.local_position = self.world_position + Vector2(
            self.width / 2 - self.label.size.x / 2, 0
        )
        self.label.render()

    def _on_redraw(self) -> None:
        """Redraw the title label by recreating the label with updated text."""
        self.label._on_redraw()


class InfoBar(Node):
    """A class that represents an information bar.

    Attributes:
        static_text (str): The static text of the bar.
        dynamic_text (str): The dynamic text of the bar.
        icon (Surface): The icon to display on the bar.
        width (int): The width of the bar.
        max_progress (int): The maximum value of the progress bar.
        reversed (bool): Whether the progress bar is reversed.
        progress_color (Color): The color of the progress bar.

    """

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
        """Initialize an InfoBar instance."""
        super().__init__(context)
        self.width = width
        self.icon = icon

        self.dynamic_text = dynamic_text
        self.static_text = static_text

        self.static_label = self.context.assets.font("ui").render(
            static_text, False, context.colors.lighter
        )
        self.dynamic_label = self.context.assets.font("ui").render(
            dynamic_text.center(5), False, context.colors.lighter
        )
        self.max_progress = max_progress

        self.last_world_pos = self.world_position
        self.progress = ProgressBar(
            self.context,
            Vector2(
                width
                - self.dynamic_label.get_size()[0] * 1.1
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
        """Update the dynamic text of the bar and progress value.

        Args:
            val (int): The new dynamic text value.

        """
        if self.reversed:
            val = self.max_progress - val
        if self.dynamic_text != str(val):
            self.dynamic_text = str(val)
            self.dynamic_label = self.context.assets.font("ui").render(
                self.dynamic_text.center(5), False, self.context.colors.lighter
            )
            self.progress.progress = val

    def _update_positions(self) -> None:
        """Update the positions of the elements."""
        self.icon_pos = self.world_position + Vector2(
            0, self.static_label.get_size()[1] * 1.2
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
        """Update the positions of the elements on position change."""
        if self.last_world_pos != self.world_position:
            self._update_positions()
            self.last_world_pos = self.world_position

    def _on_draw(self) -> None:
        """Draw the information bar elements."""
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

    def _on_redraw(self) -> None:
        """Redraw the information bar elements."""
        self.static_label = self.context.assets.font("ui").render(
            self.static_text, False, self.context.colors.lighter
        )
        self.dynamic_label = self.context.assets.font("ui").render(
            self.dynamic_text.center(5), False, self.context.colors.lighter
        )


class LivesLeft(Node):
    """A class that represents the lives left in the game.

    Attributes:
        logical_maze (LogicalMaze): The logical maze instance.
        last_level (int): The last level index.
        lives_text (Surface): The text surface for displaying lives left.

    """

    def __init__(self, context: "Context", logical_maze: LogicalMaze) -> None:
        """Initialize a LivesLeft instance."""
        super().__init__(context)

        self.logical_maze = logical_maze
        self.last_level = self.logical_maze.current_level_idx

        self.lives_text = self.context.assets.font("ui").render(
            "LIVES REMAINING: ", False, context.colors.lightest
        )

    def _on_draw(self) -> None:
        """Draw the lives left text and life icons."""
        self.context.screen.blit(
            self.lives_text,
            self.world_position,
        )
        for i in range(self.logical_maze.player.lives):
            self.context.screen.blit(
                self.context.assets.image("life_icon"),
                self.world_position + (32 * i + 25, 30),
            )

    def _on_redraw(self) -> None:
        """Redraw the lives left text."""
        self.lives_text = self.context.assets.font("ui").render(
            "LIVES REMAINING: ", False, self.context.colors.lightest
        )


class GameScene(Node):
    """A class that represents the main game scene.

    Attributes:
        logical_maze (LogicalMaze): The logical maze instance.
        maze (VisualMaze): The visual maze instance.
        score_title_label (TitleLabel): The score title label.
        level_title_label (TitleLabel): The level title label.
        time_bar (InfoBar): The time left information bar.
        gums_bar (InfoBar): The gums eaten information bar.

    """

    def __init__(self, context: Context) -> None:
        """Initialize a GameScene instance."""
        super().__init__(context)

        self.logical_maze = LogicalMaze(context.config.levels,
                                        context.config.points_per_pacgum,
                                        context.config.points_per_super_pacgum,
                                        context.config.points_per_ghost,
                                        context.config.super_pacgum_duration,
                                        lives=context.config.lives)
        self.maze = VisualMaze(
            context, self.logical_maze, level_up_callback=self._init_widgets
        )
        self._init_widgets()

    def _init_widgets(self) -> None:
        self.clear_children()
        self.maze.local_position = (
            Vector2(self.context.width, self.context.height) / 2
            - self.maze.size / 2
        )

        pause_button = Button(
            self.context,
            self.context.assets.image("pause_icon"),
            Vector2(30, 30),
            self.context.colors.lightest,
            lambda _: self.context.root_scene.add_child(
                PauseScene(self.context, self.maze)
            ),
            shadow_color=self.context.colors.light,
        )
        pause_button.local_position = Vector2(10, 10)
        gum_timer = GumTimer(self.context, self.logical_maze, 24)
        gum_timer.local_position = Vector2(
            self.maze.local_position.x - 160, 150
        )

        lives_left = LivesLeft(self.context, self.logical_maze)
        lives_left.local_position = Vector2(
            self.maze.local_position.x - 170, self.context.height - 200
        )

        self.score_title_label = TitleLabel(
            self.context,
            "SCORE: ",
            str(self.logical_maze.player.score),
            int(self.maze.size.x),
            self.context.colors.dark,
        )
        self.score_title_label.local_position = (
            self.maze.world_position - Vector2(0, 50)
        )

        self.level_title_label = TitleLabel(
            self.context,
            "LEVEL: ",
            str(self.logical_maze.current_level_idx + 1),
            int(self.maze.size.x),
            self.context.colors.darker,
        )
        self.level_title_label.local_position = (
            self.maze.world_position + Vector2(0, self.maze.size.y + 40)
        )

        self.time_bar = InfoBar(
            self.context,
            "TIME LEFT",
            "  0",
            self.context.assets.image("clock_icon"),
            int(self.context.width / 2 - self.maze.size.x / 2),
            int(self.logical_maze.ticks_remaining / 60),
            False,
            self.context.colors.light,
        )
        self.time_bar.local_position = self.maze.local_position + Vector2(
            self.maze.size.x + 10, self.maze.size.y / 2 - 76
        )

        self.gums_bar = InfoBar(
            self.context,
            "GUMS EATEN",
            "43/200",
            self.context.assets.image("gum_icon"),
            int(self.context.width / 2 - self.maze.size.x / 2),
            len(self.logical_maze.pacgums),
            True,
            self.context.colors.darker,
        )
        self.gums_bar.local_position = self.maze.local_position + Vector2(
            self.maze.size.x + 10, self.maze.size.y / 2 + 50
        )
        self.key_queue: list[int] = []
        self.cheats_enabled = False

        self.add_child(self.maze)
        self.add_child(self.score_title_label)
        self.add_child(self.level_title_label)
        self.add_child(self.time_bar)
        self.add_child(self.gums_bar)
        self.add_child(gum_timer)
        self.add_child(lives_left)
        self.add_child(pause_button)

    def _on_update(self, delta: float) -> None:
        """Update the game scene elements based on the logical maze state."""
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

    def _on_input(self, event: Event) -> Event | None:
        if event.type == pygame.KEYDOWN:
            self.key_queue.append(event.key)
            if len(self.key_queue) == 5:
                self.key_queue.pop(0)
            if self.key_queue == [
                pygame.K_KP_1,
                pygame.K_KP_3,
                pygame.K_KP_3,
                pygame.K_KP_7,
            ] or self.key_queue == [
                pygame.K_1,
                pygame.K_3,
                pygame.K_3,
                pygame.K_7,
            ]:
                self.cheats_enabled = not self.cheats_enabled
            if self.cheats_enabled:
                if event.key == pygame.K_n:
                    self.logical_maze.skip_to_next_level()
                if event.key == pygame.K_f:
                    self.logical_maze.cheat_freeze_ghosts = (
                        not self.logical_maze.cheat_freeze_ghosts
                    )
                if (
                    event.key == pygame.K_g
                    and self.logical_maze.player.state != PlayerState.DEAD
                ):
                    self.logical_maze.player.state = PlayerState.POWERED_UP
                    self.logical_maze.player.gum_timer = (
                        self.logical_maze.super_pacgum_duration
                    )
                    for ghost in self.logical_maze.ghosts:
                        if ghost.state != GhostState.DEAD:
                            ghost.state = GhostState.FRIGHTENED
                            ghost.last_direction = None
        return event
