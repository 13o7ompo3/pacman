_This project has been created as part of the 42 curriculum by atahiri-, obahya._

# Spooks

## Description:

Spooks is our Pac-Man clone in Python 3.13 and pygame. Every level is a procedurally
generated maze, the ghosts chase or flee depending on what we just ate, and the whole
game can switch between 26 color themes at runtime. Scores are saved per user and shown
on a leaderboard.

## Instructions:

### Installation:

To install the necessary dependecies, just run the appropriate make rule:

```bash
make install
```

This is equivalent to running:

```bash
uv sync
```

### Excution:

In order to run the game, simply do:

```bash
make run
```

Which is equivalent to:

```bash
uv run python pac_man.py
```

• A “Resources” section listing classic references related to the topic (documentation, articles, tutorials, etc.),
as well as a description of how AI was used —specifying for which tasks and which parts of the project.
## Resources:

### Documentation:

Since the project does not require much theory and since we were already familiar with the libraries used, we did not use any documentation for the implementation of the project. However, we did use some documentation to understand how to use the libraries and their features.

* [MiniLibX official 42 docs](https://harm-smits.github.io/42docs/libs/minilibx)
* [PyGame docs](https://www.pygame.org/docs/)

### AI Usage:

The AI was not used to write actual code, but rather it was used for boilerplate docs and as brainstrorming tool to design high level architecture and to generate ideas for the project. It was used to help with the following tasks:

* Improving the documentation of the project.
* Making the readme more readable and structured.
* rethinking the architecture of the project and generating ideas for the implementation.

## Configuration:


Config is JSON (`config.json`, passed as a CLI arg) parsed and validated by
Pydantic models in `parser.py` (`Config`, `LevelConfig`). Unknown **root** keys
are ignored; level entries are validated strictly. On any error it falls back to
safe defaults.

```json
{
  "levels": [
    { "width": 14, "height": 14, "seed": 42, "level_max_time": 12 },
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
| `levels` | 10 default level | played in order |
| `lives` | `3` | `1–5` |
| `points_per_pacgum` | `10` | |
| `points_per_super_pacgum` | `50` | |
| `points_per_ghost` | `200` | |
| `super_pacgum_duration` | `500` | FRIGHTENED ticks |

**Per-level (`LevelConfig`) defaults**

| Field | Default | Notes |
|---|---|---|
| `width` / `height` | `28` / `31` | `≥ 10` |
| `seed` | `1337` | RNG seed → reproducible maze |
| `level_max_time` | `90` | seconds (`ticks = time × 60`) |
| `speed` | `100` | `1–100`; ghosts use `speed × 0.4` |
| `pacgum` | `1337` | declared, not consumed |

> **Caveat:** the shipped `config.json` uses `level_max_timer` (typo) instead of
> `level_max_time`. Since `LevelConfig` rejects extra keys, this silently drops
> the whole `levels` array and falls back to one default level.

---

## Highscore

Implemented in `src/db_manager/user.py` via two classes:

- **`User`** (Pydantic): `username` (1–10 alnum), `password` (**SHA-256 hashed**, never plaintext), `highscore` (`≥ 0`).
- **`UserManager`**: stores one JSON file per user in `./database/`.
  - `load_all_users()` / `save_user_data()` — load & persist users.
  - `create_new_user()` / `authenticate_user()` — register or log in (sets active `loged_in_user`).
  - `update_highscore(score)` — **only if logged in and only when the new score is higher** (monotonic best-run rule); persists on change.
  - `get_leaderboard()` — users sorted by `highscore` desc.
  - `logout_user()`.

**Flow:** on game over, `GameOverScene` shows login forms — existing users are
authenticated, new ones are created, then `update_highscore(final_score)` runs.
If already logged in it offers an **Update** button. `LeaderBoardScene` shows
the top 10 via `get_leaderboard()[:10]`.

**Why this way:** file-per-user JSON keeps it dependency-light (no DB/server,
easy to inspect/back up); passwords are hashed; the "max only" rule preserves a
true best score; the model is validated (safe filenames, non-negative scores);
and the UI only calls high-level `UserManager` methods, so the storage backend
can be swapped without touching scenes.

---

## Maze Generation

Mazes come from the assigned **A-Maze-ing** package, vendored here as
`mazegenerator` (`MazeGenerator` in `mazegenerator/mazegenerator.py`), imported
by `src/logical/maze.py` via `from mazegenerator import MazeGenerator`.

- **Wall encoding:** each cell is an int whose bits are walls — `1=N, 2=E, 4=S,
  8=W`. `15` = fully solid (impassable), `0` = open.
- **`generate(seed)`** seeds RNG, builds a bordered maze with a decorative "42"
  obstacle, carves passages with a **recursive-backtracker (DFS)** (randomly
  adding loops when not `perfect`), then BFS-computes the shortest path.
- **Used by `LogicalMaze.load_level()`:**
  ```python
  self.maze_generator = MazeGenerator((self.width, self.height), seed=int(level.seed))
  self.grid = self.maze_generator.maze
  ```
  The grid is the single source of truth: `can_move()` checks wall bits per
  direction, and pellets/ghosts skip cells equal to `15`. Each level's `seed`
  makes its layout deterministic and reproducible.

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
