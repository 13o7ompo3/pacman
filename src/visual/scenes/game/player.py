import pygame
from src.visual.draw import Draw
from pygame.event import Event
from pygame import draw, Color, Vector2, KEYDOWN, image, Surface
from src.visual.utils.sprite import Sprite
from src.visual.utils.particle import ParticleSystem
from src.logical.core_types import PlayerState
from src.logical.game_event import PlayerDiedEvent, PlayerRespawnedEvent
from src.visual import Context, Node
from src.logical.maze import Direction, LogicalMaze


class Player(Node):
    def __init__(
        self,
        context: Context,
        maze: LogicalMaze,
        step_size: int,
        speed: float = 80,
    ) -> None:
        super().__init__(context)
        self.direction = None
        self.next_direction = None
        self.target_position = (
            Vector2(maze.player.x, maze.player.y) * step_size
        )
        self.animated_position = self.target_position.copy()
        self.step_size = step_size
        self.maze = maze
        self.speed = speed
        self.dead = False
        self.sprites = {
            Direction.UP: Sprite(
                context,
                self.context.assets.image("player_up"),
                1,
                4,
                10,
                True,
            ),
            Direction.DOWN: Sprite(
                context,
                self.context.assets.image("player_down"),
                1,
                4,
                10,
                True,
            ),
            Direction.LEFT: Sprite(
                context,
                self.context.assets.image("player_left"),
                1,
                4,
                10,
                True,
            ),
            Direction.RIGHT: Sprite(
                context,
                self.context.assets.image("player_right"),
                1,
                4,
                10,
                True,
            ),
        }
        self.idle_img = self.context.assets.image("player_idle")
        self.particle_img = Surface(
            (2, 2), flags=pygame.SRCALPHA
        ).convert_alpha()
        particle_color = Color(self.context.colors.lightest)
        particle_color.a = 100
        self.particle_img.fill(particle_color)
        self.particles = ParticleSystem(
            context,
            self.particle_img,
            (Vector2(10, 10), Vector2(-10, -10)),
            (Vector2(0, 0), Vector2(0, 0)),
            0.4,
            20,
        )

    def _on_input(self, event: Event) -> Event | None:
        if self.hidden:
            return
        if event.type == KEYDOWN:
            if event.key in {pygame.K_UP, pygame.K_w, pygame.K_k}:
                self.next_direction = Direction.UP
            if event.key in {pygame.K_DOWN, pygame.K_s, pygame.K_j}:
                self.next_direction = Direction.DOWN
            if event.key in {pygame.K_LEFT, pygame.K_a, pygame.K_h}:
                self.next_direction = Direction.LEFT
            if event.key in {pygame.K_RIGHT, pygame.K_d, pygame.K_l}:
                self.next_direction = Direction.RIGHT
            if self.direction is None and self.next_direction is not None:
                self.direction = self.next_direction
                player_pos = self.maze.player.get_grid_position()
                if self.maze.can_move(
                    player_pos,
                    (
                        player_pos[0] + self.direction.value[0],
                        player_pos[1] + self.direction.value[1],
                    ),
                ):
                    self.target_position = (
                        Vector2(player_pos) + self.direction.value
                    ) * self.step_size
        return event

    def _on_update(self, delta: float) -> None:
        self.particles.update(delta)
        if not self.dead:
            self.animated_position = self.animated_position.move_towards(
                self.target_position, delta * self.speed
            )
            self.particles.local_position = (
                self.world_position + self.animated_position
            )

        if self.animated_position == self.target_position:
            self._step_target_position()
        elif self.direction is not None:
            self.sprites[self.direction].update(delta)

    def _step_target_position(self):
        if self.direction is not None:
            self.maze.tick_player(self.direction)
            player_pos = self.maze.player.get_grid_position()
            if self.next_direction and self.maze.can_move_player(
                self.next_direction
            ):
                self.direction = self.next_direction
            if self.maze.can_move(
                player_pos,
                (
                    player_pos[0] + self.direction.value[0],
                    player_pos[1] + self.direction.value[1],
                ),
            ):
                self.target_position = (
                    Vector2(player_pos) + self.direction.value
                ) * self.step_size

    def respawn(self, x, y):
        self.target_position = Vector2(x, y) * self.step_size
        self.animated_position = self.target_position.copy()

    def _on_draw(self) -> None:
        self.particles.render()
        if self.direction is not None:
            sprite = self.sprites[self.direction]
            sprite.local_position = (
                self.world_position + self.animated_position
            )
            sprite.render()
        else:
            self.context.screen.blit(
                self.idle_img,
                self.world_position
                + self.animated_position
                - Vector2(self.idle_img.get_size()) / 2,
            )

    def _on_redraw(self) -> None:
        particle_color = Color(self.context.colors.lightest)
        particle_color.a = 100
        self.particle_img.fill(particle_color)
        for sprite in self.sprites.values():
            sprite.redraw()
