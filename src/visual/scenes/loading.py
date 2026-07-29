from pydantic_core.core_schema import TimeSchema
from pygame import Color, Vector2
from src.visual import Node, Context
from src.visual.scenes.title import TitleScene
from src.visual.ui.label import Label
from src.visual.ui.progress import ProgressBar, ProgressBarOrientation
from src.visual.ui.prompt import Prompt


class LoadingScene(Node):
    def __init__(self, context: Context) -> None:
        super().__init__(context)

        def on_finish(_: ProgressBar) -> None:
            self.free_from_scene()
            context.root_scene.clear_children
            title_scene = TitleScene(context)
            context.root_scene.add_child(title_scene)

        # only load the font for the loading screen
        context.assets.register_font(
            "ui", "assets/perfect_dos_vga_437.ttf", 16
        )
        context.assets.load()
        self._register_assets()

        label = Label(
            context, Vector2(256, 32), [("Loading..", Color("white"))], 2
        )
        label.local_position = (
            Vector2(context.width, context.height) / 2
            - label.size / 2
            - Vector2(0, 64)
        )

        self.progress_bar = ProgressBar(
            context,
            Vector2(256, 32),
            ProgressBarOrientation.HORIZONTAL,
            Color("orange"),
            context.assets.total_assets,
            border_radius=15,
            on_finish=on_finish,
        )
        self.progress_bar.local_position = (
            Vector2(context.width, context.height) / 2
            - self.progress_bar.size / 2
            + Vector2(0, 64)
        )

        self.loading_iter = self.context.assets.load_progress()
        self.time = 0
        self.load_time_per_item = 0.1

        self.add_child(label)
        self.add_child(self.progress_bar)

    def _on_update(self, delta: float) -> None:
        if self.time >= self.load_time_per_item:
            try:
                ret = next(self.loading_iter)
                if isinstance(ret, Exception):

                    def on_accept(_) -> None:
                        exit()

                    prompt = Prompt(self.context, "Error", str(ret), on_accept)
                    self.add_child(prompt)
                self.progress_bar.progress += 1
            except StopIteration:
                pass

            self.time = 0

        self.time += delta

    def _register_assets(self) -> None:
        self.context.assets.register_image("player_up", "assets/player/up.png")
        self.context.assets.register_image(
            "player_down", "assets/player/down.png"
        )
        self.context.assets.register_image(
            "player_left", "assets/player/left.png"
        )
        self.context.assets.register_image(
            "player_right", "assets/player/right.png"
        )
        self.context.assets.register_image(
            "player_idle", "assets/player/idle.png"
        )
        self.context.assets.register_image(
            "ghost_neutral", "assets/ghost/ghost_neutral.png"
        )
        self.context.assets.register_image(
            "ghost_running", "assets/ghost/ghost_running.png"
        )
        self.context.assets.register_image(
            "tile_ball_bottom_left", "assets/tiles/ball_bottom_left.png"
        )
        self.context.assets.register_image(
            "tile_ball_bottom_right", "assets/tiles/ball_bottom_right.png"
        )
        self.context.assets.register_image(
            "tile_ball_top_left", "assets/tiles/ball_top_left.png"
        )
        self.context.assets.register_image(
            "tile_ball_top_right", "assets/tiles/ball_top_right.png"
        )
        self.context.assets.register_image(
            "tile_bar_bottom", "assets/tiles/bar_bottom.png"
        )
        self.context.assets.register_image(
            "tile_bar_left", "assets/tiles/bar_left.png"
        )
        self.context.assets.register_image(
            "tile_bar_right", "assets/tiles/bar_right.png"
        )
        self.context.assets.register_image(
            "tile_bar_top", "assets/tiles/bar_top.png"
        )
        self.context.assets.register_image(
            "tile_corner_bottom_left", "assets/tiles/corner_bottom_left.png"
        )
        self.context.assets.register_image(
            "tile_corner_bottom_right", "assets/tiles/corner_bottom_right.png"
        )
        self.context.assets.register_image(
            "tile_corner_top_left", "assets/tiles/corner_top_left.png"
        )
        self.context.assets.register_image(
            "tile_corner_top_right", "assets/tiles/corner_top_right.png"
        )
        self.context.assets.register_image(
            "tile_empty_rect", "assets/tiles/empty_rect.png"
        )
        self.context.assets.register_image(
            "tile_full_rect", "assets/tiles/full_rect.png"
        )
