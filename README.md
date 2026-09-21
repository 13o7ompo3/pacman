_This project has been created as part of the 42 curriculum by atahiri-, obahya._

# Spooks

## Description

Spooks is our Pac-Man clone in Python 3.13 and pygame. Every level is a procedurally
generated maze, the ghosts chase or flee depending on what we just ate, and the whole
game can switch between 26 color themes at runtime. Scores are saved per user and shown
on a leaderboard.

The goal of the project is to build a complete Pac-Man on top of the assigned A-Maze-ing
maze generator: a configurable set of levels, a highscore system, and a codebase that
keeps the game rules separate from the rendering.

## Instructions

Requirements: Python 3.13 or newer and [uv](https://docs.astral.sh/uv/).

### Installation

```bash
make install        # equivalent to: uv sync
```

### Execution

```bash
make run            # equivalent to: uv run python3 pac-man.py
```

The game reads `config.json` from the current directory (see Configuration). Arrow keys
move, Escape quits.

### Other targets

```bash
make lint           # flake8 + mypy
make deploy         # PyInstaller one-file binary in dist/Spooks
make clean
```

## Resources

### Documentation and references

We mostly relied on the documentation of the libraries we used; the classic references
on the topic are listed with them.

* [pygame documentation](https://www.pygame.org/docs/)
* [pydantic documentation](https://docs.pydantic.dev/latest/), in particular
  [validators](https://docs.pydantic.dev/latest/concepts/validators/)
* [NumPy documentation](https://numpy.org/doc/) (palette swapping)
* [uv](https://docs.astral.sh/uv/) and [PyInstaller](https://pyinstaller.org/en/stable/)
* [The Pac-Man Dossier](https://www.gamedeveloper.com/design/the-pac-man-dossier):
  the reference on the original game's ghost behaviour and movement
* [Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
  and Jamis Buck's
  [Recursive Backtracking](http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
* [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) (fixed 60 Hz
  logic tick) and [Game Programming Patterns](https://gameprogrammingpatterns.com/)
  (game loop, update method, scene tree)
* [Lospec palette list](https://lospec.com/palette-list): source of the color palettes
* [dotpm for Obsidian](https://github.com/dotpm/obsidian-pm): the project management tool

### AI usage

AI was not used to write the game code. We used it for boilerplate documentation and as
a brainstorming tool for the high-level architecture. Concretely it helped with:

* Improving the docstrings of the project.
* Making this README more readable and structured.
* Rethinking the architecture and generating ideas for the implementation.
* Building the project management board and the commit timeline in
  `project_management/` from the git history.

## Configuration

The config is `config.json` in the working directory (`#` comments are allowed), parsed
and validated by the pydantic models in `src/parser.py` (`Config`, `LevelConfig`).
Unknown keys are ignored. A missing or unparsable file starts the game with the
defaults. Each field is wrapped in `FallbackToDefault`: a value of the wrong type falls
back to the field default. An out-of-range value inside a level invalidates that level
list, which then falls back to the built-in levels.

```json
{
  "levels": [
    { "width": 14, "height": 14, "seed": 42, "level_max_time": 60 },
    { "width": 15, "height": 20, "seed": 42 }
  ],
  "lives": 3,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "super_pacgum_duration": 500
}
```

**Top-level (`Config`) defaults**

| Field | Default | Notes |
|---|---|---|
| `levels` | 10 built-in levels | played in order; a shorter list is padded with the built-in ones |
| `lives` | `3` | `1-5` |
| `points_per_pacgum` | `10` | `0-20` |
| `points_per_super_pacgum` | `50` | `0-100` |
| `points_per_ghost` | `200` | `0-400` |
| `super_pacgum_duration` | `500` | FRIGHTENED duration in ticks (60 per second), `200-1000` |

**Per-level (`LevelConfig`) defaults**

| Field | Default | Notes |
|---|---|---|
| `width` / `height` | `10` / `10` | `10-22` cells |
| `seed` | `1337` | int or numeric string; `0` gives a different maze each run |
| `level_max_time` | `90` | seconds (`ticks = time * 60`) |
| `speed` | `75` | `1-200` pixels per second; ghosts move at `speed * 0.4` |
| `pacgum` | `1337` | declared, not consumed |

## Highscore

Implemented in `src/db_manager/user.py` via two classes:

- **`User`** (pydantic): `username` (1-10 characters, letters, digits and spaces),
  `password` (**SHA-256 hash**, never plaintext), `highscore` (`>= 0`).
- **`UserManager`**: stores one JSON file per user in `./database/` (git-ignored).
  - `load_all_users()` / `save_user_data()`: load and persist users, corrupt files are skipped.
  - `create_new_user()` / `authenticate_user()`: register or log in (sets `loged_in_user`).
  - `update_highscore(score)`: **only if logged in and only when the new score is higher**;
    persists on change.
  - `get_leaderboard()`: users sorted by `highscore` descending.
  - `logout_user()`.

**Flow:** on game over, `GameOverScene` shows a login form: existing users are
authenticated, new ones are created, then `update_highscore(final_score)` runs. If a
user is already logged in it offers **Update** and **Logout** buttons instead.
`LeaderBoardScene` shows the top 10 from `get_leaderboard()`.

**Why this way:** one JSON file per user keeps it dependency-free (no database, no
server, easy to inspect and back up); passwords are hashed; the "higher only" rule keeps
a true best score; the model is validated (safe filenames, non-negative scores); and the
scenes only call `UserManager` methods, so the storage could be swapped without touching
the UI.

## Maze Generation

Mazes come from the assigned **A-Maze-ing** package, vendored as the `mazegenerator`
wheel and imported by `src/logical/maze.py` with `from mazegenerator import MazeGenerator`.

- **Wall encoding:** each cell is an int whose bits are walls: `1=N, 2=E, 4=S, 8=W`.
  `15` is a fully closed cell, `0` a fully open one.
- **`generate(seed)`** seeds the RNG, builds a bordered grid, embeds a "42" made of closed
  cells when the maze is at least 14x10, carves passages with an iterative
  depth-first backtracker, and, since we keep the default `perfect=False`, braids the
  result (dead ends are opened, extra loops added) so nobody can be trapped in a
  corridor. A BFS then computes the shortest path.
- **Used by `LogicalMaze.load_level()`:**
  ```python
  self.maze_generator = MazeGenerator((self.width, self.height), seed=int(level.seed))
  self.grid = self.maze_generator.maze
  ```
  The grid is the single source of truth: `can_move()` checks the wall bit of the
  direction taken, pacgums and ghosts skip the closed `15` cells, the player spawns in
  the center, the ghosts in the four corners, the super pacgums in the corner cells.
  The seed makes every level reproducible.

## Implementation

- Two layers: `src/logical` holds the rules and never imports pygame, `src/visual` renders them.
- `LogicalMaze` owns the grid (vendored `mazegenerator`, seeded per level), the player, four
  ghosts, the pacgums and all timers. It ticks at a fixed 60 Hz, independent of the frame rate.
- Ghost AI: take the non-reversing move closest to the player (farthest when frightened), with
  a 20 percent chance of the second best so the ghosts spread out.
- Rule outcomes are frozen dataclass events (`AtePacgumEvent`, `PlayerDiedEvent`, `WinEvent`,
  ...) that the view drains once per frame with `flush_events()`.
- Everything on screen is a `Node` in a tree: `update`, `handle_input` and `render` recurse over
  the children, a node can consume an input event, scenes are swapped by replacing the root's
  children.
- Entities interpolate between cell centers with `delta * speed` and call `tick_player` /
  `tick_ghost` on arrival; collisions are distance checks with our own `Vec2`.
- We draw with our own `Draw` engine (rects, rounded rects, sectors, circles, alpha), cut
  sprites from PNG atlases, use a 9x16 bitmap font and store a theme as a 6x1 PNG palette.
  Switching theme recolors every loaded asset with numpy masks.
- `config.json` (JSON with `#` comments) is validated by pydantic; a `FallbackToDefault` wrap
  validator swaps any invalid field for its default, so a broken file still starts the game.
- `UserManager` stores one JSON per user with a SHA-256 password hash and the highscore.
- Cheats unlock with a hashed key sequence: `N` next level, `F` freeze ghosts, `G` power-up.
- Tooling: uv, flake8, mypy, PyInstaller one-file binary.

## General Software Architecture

```
pac-man.py               main loop: input -> update -> render
src/parser.py            Config, LevelConfig (pydantic)
src/db_manager/user.py   User, UserManager
src/logical/             Direction, GhostState, PlayerState | Entity -> Player, Ghost
                         GameEvent -> 10 event types | LogicalMaze
src/visual/              GameComponent -> Node | Context | Draw | ColorPalette
  scenes/                RootScene, LoadingScene, TitleScene, PauseScene, GameOverScene,
                         LeaderBoardScene, InstructionsScene,
                         game/: GameScene, VisualMaze, Player, VisualGhost, InfoBar
  ui/                    Button, Label, Panel, ProgressBar, Prompt, TextBox
  utils/                 AssetManager, Font, Image, Vec2, Rect, Sprite, ParticleSystem,
                         Parallax, Shake, Timer
```

```
pygame events / clock --> RootScene --> GameScene --> VisualMaze --> LogicalMaze
                                                         ^  ticks it at 60 Hz, flushes its
                                                         |  events into particles, shake,
                                                         |  freeze frames and scene changes
```

- Every scene, widget, entity and effect is a `Node`; `Context` (screen, assets, palette,
  users, config) is handed to each one.
- `GameScene` builds one `LogicalMaze` and a `VisualMaze`, which binds a `Player` and a
  `VisualGhost` to each logical entity.
- Dependencies point one way: `visual` -> `logical` -> `mazegenerator`; only `pac-man.py`
  imports `visual`.

## Project Management

Two of us: atahiri- (Blxee) on the visual layer and tooling, obahya (13o7ompo3) on the game
logic, config and persistence. We worked on `feat/<topic>` branches merged into `main`, with
small verb-prefixed commits (Added, Fixed, Changed) and `make lint` as the merge gate. The
295 commits (2026-06-24 to 2026-09-21) fall into eight phases, each closed by a milestone:
first playable build, own draw engine, full theme support, game juice, lint clean, release.

We track it in Obsidian with the dotpm plugin, in [project_management/](project_management/):
the [project board](project_management/Projects/Spooks/Spooks.md) (phases, subtasks,
milestones, backlog), the [people notes](project_management/People/) and the
[commit timeline](project_management/timeline.md) it was built from.

