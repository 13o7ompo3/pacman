"""The loading scene is responsible for loading all the assets."""

from pygame import Vector2
from src.visual import Node, Context
from src.visual.scenes.title import TitleScene
from src.visual.ui.label import Label
from src.visual.ui.progress import ProgressBar, ProgressBarOrientation
from src.visual.ui.prompt import Prompt


class LoadingScene(Node):
    """A class that represents the loading scene.

    Attributes:
        progress_bar (ProgressBar): The progress bar of the loading scene.
        loading_iter (iter): An iterator for loading assets.
        time (float): The time elapsed since the last asset was loaded.
        load_time_per_item (float): The time to wait before loading the next.

    """

    def __init__(self, context: Context) -> None:
        """Initialize a LoadingScene instance."""
        super().__init__(context)

        def on_finish(_: ProgressBar) -> None:
            """Handle the completion of asset loading."""
            self.free_from_scene()
            self.context.root_scene.finish_loading()
            title_scene = TitleScene(context)
            context.root_scene.add_child(title_scene)

        # only load the font for the loading screen
        context.assets.register_font(
            "ui", "assets/perfect_dos_vga_437.ttf", 16
        )
        context.assets.load()
        self._register_assets()

        label = Label(
            context,
            Vector2(256, 32),
            [("Loading..", context.colors.lightest)],
            2,
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
            context.colors.light,
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
        self.load_time_per_item = 0

        self.add_child(label)
        self.add_child(self.progress_bar)

    def _on_update(self, delta: float) -> None:
        """Update the loading scene.

        Args:
            delta (float): The time elapsed since the last update.

        """
        if self.time >= self.load_time_per_item:
            try:
                ret = next(self.loading_iter)
                if isinstance(ret, Exception):

                    def on_accept(_) -> None:
                        """Handle the acceptance of the error prompt."""
                        self.context.game_running = False

                    prompt = Prompt(self.context, "Error", str(ret), on_accept)
                    self.add_child(prompt)
                else:
                    self.progress_bar.progress += 1
            except StopIteration:
                pass

            self.time = 0

        self.time += delta

    def _register_assets(self) -> None:
        """Register all the assets to be loaded."""
        # load animations
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
            "player_silhouette", "assets/player/silhouette.png"
        )
        self.context.assets.register_image(
            "ghost_neutral", "assets/ghost/ghost_neutral.png"
        )
        self.context.assets.register_image(
            "ghost_running", "assets/ghost/ghost_running.png"
        )

        # load tileset
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

        # load tiles
        self.context.assets.register_image(
            "clock_icon", "assets/icons/clock.png"
        )
        self.context.assets.register_image("gum_icon", "assets/icons/gum.png")
        self.context.assets.register_image(
            "life_icon", "assets/icons/life.png"
        )
        self.context.assets.register_image(
            "play_icon", "assets/icons/play.png"
        )
        self.context.assets.register_image("cup_icon", "assets/icons/cup.png")
        self.context.assets.register_image(
            "exit_icon", "assets/icons/exit.png"
        )
        self.context.assets.register_image(
            "pause_icon", "assets/icons/pause.png"
        )
        self.context.assets.register_image(
            "return_icon", "assets/icons/return.png"
        )
        self.context.assets.register_image(
            "login_icon", "assets/icons/login.png"
        )
        self.context.assets.register_image(
            "update_icon", "assets/icons/update.png"
        )
        self.context.assets.register_image(
            "instructions_icon", "assets/icons/instructions.png"
        )
        self.context.assets.register_image(
            "next_icon", "assets/icons/next.png"
        )
        self.context.assets.register_image(
            "previous_icon", "assets/icons/previous.png"
        )

        # load palettes
        # self.context.assets.register_image(
        #     "oil-6_palette", "assets/palettes/oil-6-1x.png"
        # )
        self.context.assets.register_image(
            "2sois-1x", "assets/palettes/2sois-1x.png"
        )
        self.context.assets.register_image(
            "6353yh4-redux-1x", "assets/palettes/6353yh4-redux-1x.png"
        )
        self.context.assets.register_image(
            "6-violets-1x", "assets/palettes/6-violets-1x.png"
        )
        self.context.assets.register_image(
            "ash-persimmon-6-1x", "assets/palettes/ash-persimmon-6-1x.png"
        )
        self.context.assets.register_image(
            "autumn-decay-1x", "assets/palettes/autumn-decay-1x.png"
        )
        self.context.assets.register_image(
            "berries-and-cream-1x", "assets/palettes/berries-and-cream-1x.png"
        )
        self.context.assets.register_image(
            "black-and-white-6-1x", "assets/palettes/black-and-white-6-1x.png"
        )
        self.context.assets.register_image(
            "blackhole6-1x", "assets/palettes/blackhole6-1x.png"
        )
        self.context.assets.register_image(
            "bluberry-6-1x", "assets/palettes/bluberry-6-1x.png"
        )
        self.context.assets.register_image(
            "blue-newspaper-1x", "assets/palettes/blue-newspaper-1x.png"
        )
        self.context.assets.register_image(
            "blue-screen-of-palette-1x",
            "assets/palettes/blue-screen-of-palette-1x.png",
        )
        self.context.assets.register_image(
            "brazil-flag-1x", "assets/palettes/brazil-flag-1x.png"
        )
        self.context.assets.register_image(
            "bronze-palette-1x", "assets/palettes/bronze-palette-1x.png"
        )
        self.context.assets.register_image(
            "calm-n-chloric-1x", "assets/palettes/calm-n-chloric-1x.png"
        )
        self.context.assets.register_image(
            "carver6-1x", "assets/palettes/carver6-1x.png"
        )
        self.context.assets.register_image(
            "cave6-1x", "assets/palettes/cave6-1x.png"
        )
        self.context.assets.register_image(
            "ciboulette-6-1x", "assets/palettes/ciboulette-6-1x.png"
        )
        self.context.assets.register_image(
            "city-street-6-1x", "assets/palettes/city-street-6-1x.png"
        )
        self.context.assets.register_image(
            "cloudfrenzy-1x", "assets/palettes/cloudfrenzy-1x.png"
        )
        self.context.assets.register_image(
            "clown-cake-1x", "assets/palettes/clown-cake-1x.png"
        )
        self.context.assets.register_image(
            "compliment6-1x", "assets/palettes/compliment6-1x.png"
        )
        self.context.assets.register_image(
            "crabs-orange-red-palette-1x",
            "assets/palettes/crabs-orange-red-palette-1x.png",
        )
        self.context.assets.register_image(
            "cryptic-ocean-1x", "assets/palettes/cryptic-ocean-1x.png"
        )
        self.context.assets.register_image(
            "curiosities-1x", "assets/palettes/curiosities-1x.png"
        )
        self.context.assets.register_image(
            "cybergum6-1x", "assets/palettes/cybergum6-1x.png"
        )
        self.context.assets.register_image(
            "cyclope6-1x", "assets/palettes/cyclope6-1x.png"
        )
        self.context.assets.register_image(
            "depths-1x", "assets/palettes/depths-1x.png"
        )
        self.context.assets.register_image(
            "discordant-6-1x", "assets/palettes/discordant-6-1x.png"
        )
        self.context.assets.register_image(
            "dnot-froget-1x", "assets/palettes/dnot-froget-1x.png"
        )
        self.context.assets.register_image(
            "eggdealer6-1x", "assets/palettes/eggdealer6-1x.png"
        )
        self.context.assets.register_image(
            "eibre-19-1x", "assets/palettes/eibre-19-1x.png"
        )
        self.context.assets.register_image(
            "enbydiade6-1x", "assets/palettes/enbydiade6-1x.png"
        )
        self.context.assets.register_image(
            "enchanted-6-1x", "assets/palettes/enchanted-6-1x.png"
        )
        self.context.assets.register_image(
            "extinction-1x", "assets/palettes/extinction-1x.png"
        )
        self.context.assets.register_image(
            "fistat6-1x", "assets/palettes/fistat6-1x.png"
        )
        self.context.assets.register_image(
            "grape-soda-arcade-1x", "assets/palettes/grape-soda-arcade-1x.png"
        )
        self.context.assets.register_image(
            "greedpit-1x", "assets/palettes/greedpit-1x.png"
        )
        self.context.assets.register_image(
            "hope-diamond-1x", "assets/palettes/hope-diamond-1x.png"
        )
        self.context.assets.register_image(
            "ice-cream-land-1x", "assets/palettes/ice-cream-land-1x.png"
        )
        self.context.assets.register_image(
            "ice-cream-spice-1x", "assets/palettes/ice-cream-spice-1x.png"
        )
        self.context.assets.register_image(
            "icywitch-1x", "assets/palettes/icywitch-1x.png"
        )
        self.context.assets.register_image(
            "inkpink-1x", "assets/palettes/inkpink-1x.png"
        )
        self.context.assets.register_image(
            "joker-6-1x", "assets/palettes/joker-6-1x.png"
        )
        self.context.assets.register_image(
            "lavendertown-1x", "assets/palettes/lavendertown-1x.png"
        )
        self.context.assets.register_image(
            "lv-weaver-801-1x", "assets/palettes/lv-weaver-801-1x.png"
        )
        self.context.assets.register_image(
            "midnight-epipelagic-1x",
            "assets/palettes/midnight-epipelagic-1x.png",
        )
        self.context.assets.register_image(
            "monometalic-1x", "assets/palettes/monometalic-1x.png"
        )
        self.context.assets.register_image(
            "noelles-room-1x", "assets/palettes/noelles-room-1x.png"
        )
        self.context.assets.register_image(
            "pink-neon-sign-6-1x", "assets/palettes/pink-neon-sign-6-1x.png"
        )
        self.context.assets.register_image(
            "puffball-6-1x", "assets/palettes/puffball-6-1x.png"
        )
        self.context.assets.register_image(
            "retro-perfect-1x", "assets/palettes/retro-perfect-1x.png"
        )
        self.context.assets.register_image(
            "robots-are-cool-1x", "assets/palettes/robots-are-cool-1x.png"
        )
        self.context.assets.register_image(
            "roserust-1x", "assets/palettes/roserust-1x.png"
        )
        self.context.assets.register_image(
            "sailers-friday-1x", "assets/palettes/sailers-friday-1x.png"
        )
        self.context.assets.register_image(
            "sandy-06-1x", "assets/palettes/sandy-06-1x.png"
        )
        self.context.assets.register_image(
            "seoul-city-1x", "assets/palettes/seoul-city-1x.png"
        )
        self.context.assets.register_image(
            "sepia6-1x", "assets/palettes/sepia6-1x.png"
        )
        self.context.assets.register_image(
            "septembit-23-1x", "assets/palettes/septembit-23-1x.png"
        )
        self.context.assets.register_image(
            "snail-village-1x", "assets/palettes/snail-village-1x.png"
        )
        self.context.assets.register_image(
            "spooky6-1x", "assets/palettes/spooky6-1x.png"
        )
        self.context.assets.register_image(
            "teaviie-1x", "assets/palettes/teaviie-1x.png"
        )
        self.context.assets.register_image(
            "unicorn-6-1x", "assets/palettes/unicorn-6-1x.png"
        )
        self.context.assets.register_image(
            "vintage-voltage-1x", "assets/palettes/vintage-voltage-1x.png"
        )
        self.context.assets.register_image(
            "yamazaki-1x", "assets/palettes/yamazaki-1x.png"
        )

        # load instructions
        self.context.assets.register_image(
            "movements_instruction", "assets/instructions/movements.png"
        )
        self.context.assets.register_image(
            "losing_instruction", "assets/instructions/losing.png"
        )
        self.context.assets.register_image(
            "super_pacgum_instruction", "assets/instructions/super_pacgum.png"
        )
        self.context.assets.register_image(
            "winning_instruction", "assets/instructions/winning.png"
        )

        # load background layers
        self.context.assets.register_image(
            "background_layer1", "assets/parallax/layer_1.png"
        )
        self.context.assets.register_image(
            "background_layer2", "assets/parallax/layer_2.png"
        )
        self.context.assets.register_image(
            "background_layer3", "assets/parallax/layer_3.png"
        )
        self.context.assets.register_image(
            "background_layer4", "assets/parallax/layer_4.png"
        )
