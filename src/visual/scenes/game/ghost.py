from src.logical.core_types import GhostState
from src.visual.utils.particle import ParticleSystem
import pygame
from src.logical.entities import Ghost
from src.visual.draw import Draw
from src.logical.game_event import AteGhostEvent
from src.logical.maze import LogicalMaze
from src.visual import Node, Context
from src.visual.utils.sprite import Sprite
from pygame import Surface, draw, Color, Vector2, image, sprite


class VisualGhost(Node):
    def __init__(
        self,
        context: Context,
        id: int,
        maze: LogicalMaze,
        ghost: Ghost,
        step_size: int,
        speed: float,
    ) -> None:
        super().__init__(context)
        self.id = id
        self.logical_maze = maze
        self.logical_ghost = ghost
        self.step_size = step_size
        self.target_position = Vector2(ghost.x, ghost.y) * step_size
        self.animated_position = self.target_position.copy()

        self.ghost_step_timer = 0
        self.speed = speed
        self.ghost_step_duration = step_size / self.speed

        self.sprite_neutral = Sprite(
            context,
            context.assets.image("ghost_neutral"),
            1,
            2,
            5,
            True,
        )
        self.sprite_running = Sprite(
            context,
            context.assets.image("ghost_running"),
            1,
            4,
            17,
            True,
        )
        particle_img = Surface((1, 1), flags=pygame.SRCALPHA)
        particle_color = Color("white")
        particle_color.a = 100
        particle_img.fill(particle_color)
        self.particles = ParticleSystem(
            context,
            particle_img,
            (Vector2(10, 10), Vector2(-10, -10)),
            (Vector2(0, 0), Vector2(0, 0)),
            0.4,
            20,
        )

    def _on_update(self, delta: float) -> None:
        match self.logical_ghost.state:
            case GhostState.FRIGHTENED:
                current_sprite = self.sprite_running
                self.particles.update(delta)
            case _:
                current_sprite = self.sprite_neutral
        current_sprite.update(delta)
        current_sprite.flip_x = (
            self.animated_position.x < self.target_position.x
        )
        self.particles.local_position = (
            self.world_position + self.animated_position
        )
        self.ghost_step_timer += delta
        if self.ghost_step_timer > self.ghost_step_duration:
            self.logical_maze.tick_ghost(self.id)
            self.ghost_step_timer = 0

        self.target_position = (
            Vector2(self.logical_ghost.x, self.logical_ghost.y)
            * self.step_size
        )
        self.animated_position = self.animated_position.move_towards(
            self.target_position, self.speed * delta
        )

    def _on_draw(self) -> None:
        match self.logical_ghost.state:
            case GhostState.FRIGHTENED:
                current_sprite = self.sprite_running
                self.particles.render()
            case _:
                current_sprite = self.sprite_neutral
        current_sprite.local_position = (
            self.world_position + self.animated_position
        )
        current_sprite.render()

    def respawn(self, x, y):
        self.target_position = Vector2(x, y) * self.step_size
        self.animated_position = self.target_position.copy()
        self.dead = False

    def _on_redraw(self) -> None:
        self.sprite_neutral.redraw()
        self.sprite_running.redraw()
