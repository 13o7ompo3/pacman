# Pacman Timeline - Condensed Commits

## Overview

| Item                     | Value                                                       |
| ------------------------ | ----------------------------------------------------------- |
| Commits on `main`        | 295 (227 regular + 68 merge commits)                        |
| Stack                    | Python 3.13, pygame, pydantic, numpy, uv, PyInstaller, flake8, mypy |
| Codebase                 | about 7300 lines of Python in `src/` plus 79 asset files (26 color palettes) |
| Workflow                 | 25 `feat/*` branches merged back into `main` (ui, gameplay, logical_maze, sprite, tileset, image, parallax, particle, cheat, config, docs, lint, ...) |

### Rough division:

**obahya** owns the pure game logic (`src/logical`), the config
parser, the user database and low-level image/particle utilities.  
**atahiri-** owns the visual
layer (scene tree, UI widgets, draw engine, scenes, assets, themes, game feel).

Activity by month: June 1 commit, July 167, August 76, September 51.

## The 15 milestones that matter most

| Date       | Commit    | Milestone                                                              |
| ---------- | --------- | ---------------------------------------------------------------------- |
| 2026-06-24 | `0b03d1f` | First commit: vendored "A-Maze-ing" maze generator package             |
| 2026-07-05 | `3b3228b` | Project bootstrapped with uv, pygame and pydantic; `pac-man.py` entry point |
| 2026-07-05 | `9642962` | Node class: the scene tree architecture every visual object is built on |
| 2026-07-10 | `f21d2c4` | "game logic !!": full logical maze rewrite (states, ticks, ghosts, player) |
| 2026-07-13 | `9232533` | Scene switching: Title, Leaderboard and Game scenes                    |
| 2026-07-16 | `a3e9023` | feat/gameplay merged into main: first end-to-end playable build        |
| 2026-07-19 | `34a7d4f` | Start of the custom draw engine (`src/visual/draw.py`)                 |
| 2026-07-26 | `dcdc177` | Maze rendered with tile images instead of primitives                   |
| 2026-07-29 | `29501c8` | AssetManager plus LoadingScene: centralized asset loading              |
| 2026-07-29 | `0bb8fab` | Global palette and theme switching                                     |
| 2026-08-01 | `5429ee5` | Cheat mode unlocked by a secret key combination                        |
| 2026-08-08 | `f9f718a` | "Game juice": particles, screen shake, hit-freeze                       |
| 2026-09-05 | `8980545` | Game speed decoupled from frame rate (fixed 60 Hz logic tick)          |
| 2026-09-14 | `20f6c64` | Zero mypy errors (same day: zero flake8 errors, docstrings everywhere) |
| 2026-09-18 | `25b37c9` | Migration to a home-made Vector primitive across 23 files              |

## Detailed timeline

Legend for the Author column: A = **atahiri-**, O = **obahya**.

### Phase 0 - Standalone building blocks (2026-06-24 to 2026-07-04)

Three utilities are written before any game code exists.

| Date       | Commit    | Author | In a nutshell                                                        |
| ---------- | --------- | ------ | -------------------------------------------------------------------- |
| 2026-06-24 | `0b03d1f` | O      | Vendored the external "A-Maze-ing" package (`MazeGenerator` class: seeded, perfect/imperfect mazes, shortest path) |
| 2026-07-04 | `12b5a20` | O      | JSON-with-comments config parser (`parser.py`)                       |
| 2026-07-04 | `f3803d2` | O      | First users database manager (`user.py`)                             |

### Phase 1 - Bootstrap and engine skeleton (2026-07-05 to 2026-07-09)

| Date       | Commit    | Author | In a nutshell                                                        |
| ---------- | --------- | ------ | -------------------------------------------------------------------- |
| 2026-07-05 | `3b3228b` | A      | uv project initialized (pyproject, lock file, `pac-man.py`, deps: pygame, pydantic) |
| 2026-07-05 | `de3e726` | A      | Scaffold for game components and screen (`src/visual`)              |
| 2026-07-05 | `9642962` | A      | `Node` / `GameComponent` classes: scene tree with update, input and render passes |
| 2026-07-05 | `248cea0` | O      | `src/logical/maze.py`: maze generation plus ghost path finding       |
| 2026-07-05 | `483e606` | A      | First visual maze drawing (`GameScene`)                              |
| 2026-07-05 | `1a0dd0e` | O      | Ghost and player movement logic, normal pacgum placement             |
| 2026-07-05 | `a48b291` | A      | First UI widget: `Button`                                            |
| 2026-07-06 | `52f2b29` | A      | Makefile (install / run rules)                                       |
| 2026-07-06 | `b1783eb` | A      | Button widget finished (highlight/shadow colors, stuck-press fix followed) |
| 2026-07-07 | `e2d023b` | A      | `Context` object holding global game data (width, height, font, ...) |
| 2026-07-09 | `b34c239` | A      | `make deploy`: PyInstaller one-file windowed binary with bundled assets |
| 2026-07-09 | `72e2244` | A      | Nodes can consume input events so they stop propagating to parents   |

### Phase 2 - Core gameplay loop (2026-07-10 to 2026-07-16)

| Date       | Commit    | Author | In a nutshell                                                        |
| ---------- | --------- | ------ | -------------------------------------------------------------------- |
| 2026-07-10 | `9211bf2` | O      | Switched to the standard `logging` module                            |
| 2026-07-10 | `f21d2c4` | O      | "game logic !!": major rewrite of the logical maze (+377/-116): `GhostState`, `PlayerState`, `TickEvent`, `RenderState` |
| 2026-07-10 | `c72cc07` | O      | Logic split into `core_types.py`, `entities.py`, `maze.py`           |
| 2026-07-10 | `4bd0636` | A      | Player no longer moves through walls                                 |
| 2026-07-10 | `c2b73b1` | A      | Basic player animation                                               |
| 2026-07-10 | `cb28140` | A      | Movement feel aligned with the real Pac-Man (persistent motion, queued turns) |
| 2026-07-11 | `c9cb5f7` | A      | Ghosts and pacgums drawn on screen (`ghost.py`, `player.py` visual entities) |
| 2026-07-11 | `6f7e7ee` | A      | Ghosts no longer pass through walls                                  |
| 2026-07-11 | `215c582` | A      | Dynamic `Label` widget                                               |
| 2026-07-12 | `ff1c7eb` | O      | Player and ghost auto-respawn after a delay (respawn events)         |
| 2026-07-13 | `9232533` | A      | Scene switching: `Title`, `Leaderboard` and `Game` scenes            |
| 2026-07-13 | `34d5f58` | A      | Pause screen and `Panel` widget                                      |
| 2026-07-14 | `f60ed61` | O      | New `GameEvent` object model (`game_event.py`)                       |
| 2026-07-14 | `6c4dabe` | O      | `TickEvent` enum replaced by `GameEvent` objects                     |
| 2026-07-14 | `5995181` | A      | Prompt / alert widget finished                                       |
| 2026-07-14 | `19d7dc9` | A      | Maze drawn centered on the screen                                    |
| 2026-07-15 | `1a27ec2` | A      | Progress bar for level completion (`progress.py`)                    |
| 2026-07-15 | `7f975e9` | A      | Each ghost handles its own time tick                                 |
| 2026-07-16 | `f343303` | O      | Events are accumulated and flushed in batches                        |
| 2026-07-16 | `985381d` | O      | New DB manager with an authentication system (`src/db_manager/user.py`) |
| 2026-07-16 | `c08dbc4` | A      | New event system integrated into the visual layer                    |
| 2026-07-16 | `a3e9023` | A      | feat/gameplay merged into main: first playable build                 |
| 2026-07-16 | `a28dc91` | A      | Leaderboard implemented                                              |
| 2026-07-16 | `08493f4` | A      | Game over screen started, `TextBox` widget introduced                |

### Phase 3 - Progression, accounts and custom draw engine (2026-07-17 to 2026-07-25)

| Date       | Commit    | Author | In a nutshell                                                        |
| ---------- | --------- | ------ | -------------------------------------------------------------------- |
| 2026-07-17 | `4bed19c` | O      | `WinEvent` emitted when all levels are completed                     |
| 2026-07-17 | `03690e9` | O      | Levels passed as argument to the logic; end of game handled          |
| 2026-07-18 | `819adb2` | A      | Score-saving form (login / register) on game over                    |
| 2026-07-18 | `a98c452` | A      | Error prompts for wrong credentials                                  |
| 2026-07-19 | `87d4aa4` | A      | Persistent login and logout                                          |
| 2026-07-19 | `34a7d4f` | A      | Custom rect drawing function: birth of `src/visual/draw.py`          |
| 2026-07-19 | `7e5517e` | A      | Sector (pie slice) drawing                                           |
| 2026-07-20 | `e2aa87a` | O      | Rounded rectangle drawing                                            |
| 2026-07-20 | `004afd4` | A      | Level-up flow                                                        |
| 2026-07-20 | `6d5f5f6` | A      | Game won screen; quit button on game over screen                     |
| 2026-07-22 | `5d23a37` | O      | Ghost next move is pre-computed                                      |
| 2026-07-22 | `7d11e17` | A      | Draw module refactored: one function for rect and round rect         |
| 2026-07-23 | `297567c` | A      | Border thickness for all rectangle types                             |
| 2026-07-23 | `918de00` | A      | Circle drawing                                                       |
| 2026-07-23 | `cb6e511` | A      | Migration to the in-house draw engine completed                      |
| 2026-07-23 | `916c133` | A      | Sprite animation class blueprint (`sprite.py`)                       |
| 2026-07-24 | `bd14e69` | O      | Core sprite logic; subsurface and flip helpers followed (`34808f5`)  |
| 2026-07-25 | `4208664` | O      | `ParticleSystem` (single surface, velocity and acceleration ranges)  |
| 2026-07-25 | `7fe61c4` | A      | Password masked while typing                                         |
| 2026-07-25 | `79defeb` | A      | Transparency support in the draw engine                              |

### Phase 4 - Art pipeline: tiles, sprites, assets and themes (2026-07-26 to 2026-08-01)

| Date       | Commit    | Author | In a nutshell                                                        |
| ---------- | --------- | ------ | -------------------------------------------------------------------- |
| 2026-07-26 | `f39c700` | A      | New in-game HUD layout (score, lives, timer widgets)                 |
| 2026-07-26 | `dcdc177` | O      | Maze drawn with tile images                                          |
| 2026-07-27 | `c5b0cf0` | A      | Tileset assets reworked                                              |
| 2026-07-27 | `2142652` | A      | Player sprite assets                                                 |
| 2026-07-27 | `892f149` | A      | Walking particles behind the player                                  |
| 2026-07-28 | `16e0883` | A      | Buttons can show an icon next to text                                |
| 2026-07-28 | `878df66` | A      | Ghost sprites                                                        |
| 2026-07-29 | `29501c8` | A      | `AssetManager` plus `LoadingScene` (centralized loading, error handling) |
| 2026-07-29 | `2740bb8` | O      | `Image` class for pixel manipulation (numpy added as dependency)     |
| 2026-07-29 | `0bb8fab` | A      | Global palette and the ability to change theme (`palette.py`)        |
| 2026-07-30 | `b9a78b6` | O      | Ghost direction / next move reset when the player dies               |
| 2026-07-30 | `2f01bb4` | O      | Parallax background (`parallax.py`)                                  |
| 2026-07-30 | `5dc7741` | A      | Dynamic color theme change; `RootScene` introduced                   |
| 2026-07-30 | `c15b2ec` | O      | Image palette swapping                                               |
| 2026-07-31 | `03d3b03` | A      | Full palette change applied to the entire game                       |
| 2026-07-31 | `5be8880` | A      | Instructions scene blueprint (first panel same day, `f606ff8`)       |
| 2026-08-01 | `7126ea1` | A      | Old assets converted to the new default theme                        |
| 2026-08-01 | `5429ee5` | O      | Cheat mode toggled by a secret key sequence (next level, freeze ghosts, ...) |
| 2026-08-01 | `afcc953` | A      | Third and last instructions page                                     |

### Phase 5 - Config, documentation, polish and game feel (2026-08-02 to 2026-08-08)

| Date       | Commit    | Author | In a nutshell                                                        |
| ---------- | --------- | ------ | -------------------------------------------------------------------- |
| 2026-08-02 | `02c688e` | O      | Docstrings for the logic modules                                     |
| 2026-08-03 | `8e354a8` | A      | Player drifting glitch fixed                                         |
| 2026-08-03 | `60fc0d6` | A      | Docstrings for most visual modules (game module in `1997943`)        |
| 2026-08-03 | `e8942bd` | A      | Most flake8 errors fixed in the visual modules                       |
| 2026-08-04 | `01e4265` | O      | `Config` and `LevelConfig` classes                                   |
| 2026-08-04 | `38b8c78` | O      | Ghost movement updated                                               |
| 2026-08-04 | `baa72d2` | O      | `play` / `stop` on the particle system                               |
| 2026-08-04 | `b6b3284` | A      | GameScene repositions itself after level up                          |
| 2026-08-04 | `75c832a` | A      | HUD becomes dynamic when the level changes                           |
| 2026-08-05 | `d6c3da0` | O      | More per-level config parameters (speed and lives wired in `a7bcf86`, `a85ad40`) |
| 2026-08-05 | `d3e4285` | O      | Cheat code is now compared by hash instead of plain key list         |
| 2026-08-05 | `4e7261b` | O      | End of level detected in `tick_timers` rather than in item collisions |
| 2026-08-05 | `2cae8de` | A      | Trail effect after eating a super pacgum                             |
| 2026-08-05 | `c3f88be` | A      | Parallax layers in the game scene (clearing bug fixed in `486ebfa`)  |
| 2026-08-06 | `9a142f9` | A      | Widgets no longer pushed off screen on large levels                  |
| 2026-08-06 | `f5ac938` | A      | Parallax dims and slows down during gameplay                         |
| 2026-08-06 | `f1e1dec` | O      | Cheat mode persists across levels                                    |
| 2026-08-06 | `77ffed0` | A      | Palette selection started (bulk import of palette PNGs)              |
| 2026-08-07 | `017bf7a` | O      | 10 levels defined                                                    |
| 2026-08-07 | `8c07c44` | A      | Curated set of 20+ themes; theme icon                                |
| 2026-08-07 | `375ea21` | A      | Change theme button                                                  |
| 2026-08-07 | `a536521` | A      | Separate font for the title                                          |
| 2026-08-08 | `d528cdf` | A      | Screen shake utility (`shake.py`); pygame hello message hidden       |
| 2026-08-08 | `5a71d35` | A      | Pacgum assets                                                        |
| 2026-08-08 | `fcce0ce` | A      | `Timer` component                                                    |
| 2026-08-08 | `187a0e1` | A      | Short freeze frame when eating a ghost                               |
| 2026-08-08 | `f9f718a` | A      | "Game juice" pass: particles, shake and freeze wired into player, ghost and maze |

Then a 4-week pause (no commits between 2026-08-09 and 2026-09-04).

### Phase 6 - Stabilization, lint and type safety (2026-09-05 to 2026-09-14)

| Date       | Commit    | Author | In a nutshell                                                        |
| ---------- | --------- | ------ | -------------------------------------------------------------------- |
| 2026-09-05 | `8980545` | A      | Game speed no longer depends on frame rate: logic ticks at a fixed 60 Hz |
| 2026-09-05 | `21eb3ce` | A      | Game no longer continues after the level timer runs out              |
| 2026-09-08 | `cfb1ac6` | A      | Ctrl-C (KeyboardInterrupt) handled cleanly                           |
| 2026-09-11 | `f64747b` | A      | Theme could be changed from the instructions screen: fixed           |
| 2026-09-14 | `53dd241` | A      | Window / game icon                                                   |
| 2026-09-14 | `202979e` | A      | Lint rules in the Makefile (`make lint`, `make lint-strict`)         |
| 2026-09-14 | `edb8c12` | A      | Custom blit removed                                                  |
| 2026-09-14 | `d1a2390` | A      | Docstrings fixed for the whole visual layer (25 files)               |
| 2026-09-14 | `76c9d94` | A      | Docstrings for all remaining Python code                             |
| 2026-09-14 | `a874802` | A      | All flake8 errors fixed                                              |
| 2026-09-14 | `ccc8ebc` | O      | `__init__.py` files added to make packages explicit (mypy)           |
| 2026-09-14 | `46affda` | O      | mypy errors fixed in `src/logical`                                   |
| 2026-09-14 | `20f6c64` | A      | All mypy errors fixed                                                |

### Phase 7 - Physics rewrite and final polish (2026-09-17 to 2026-09-21)

| Date       | Commit    | Author | In a nutshell                                                        |
| ---------- | --------- | ------ | -------------------------------------------------------------------- |
| 2026-09-17 | `be69bfa` | A      | New physics-based collision detection (work in progress)             |
| 2026-09-17 | `a3dfc3d` | A      | Dynamic lives in cheat mode                                          |
| 2026-09-18 | `25b37c9` | A      | Migration to a home-made `Vector` (`primitives.py`), touching 23 files |
| 2026-09-18 | `953c623` | A      | Parallax freeze fixed                                                |
| 2026-09-18 | `146f496` | A      | New `Rectangle` primitive                                            |
| 2026-09-19 | `c34e472` | A      | Title switched from a font to a PNG banner                           |
| 2026-09-19 | `6769a07` | A      | Custom bitmap font (`font.py`)                                       |
| 2026-09-19 | `dea26be` | O      | Config parser rewritten on pydantic with a `FallbackToDefault` validator; moved to `src/parser.py` (imports fixed in `60ee3c7`) |
| 2026-09-19 | `071325d` | A      | Super pacgums now spawn in the corners                               |
| 2026-09-19 | `d48c586` | A      | Collision detection fixed                                            |
| 2026-09-20 | `6b631bf` | O      | Collision detection fixed again; player/ghost teleporting fixed (`6f26a3d`) |
| 2026-09-20 | `d21afdc` | A      | Win screen and parallax improved                                     |
| 2026-09-20 | `edd6eb4` | A      | Maze hidden when the game over screen appears                        |
| 2026-09-20 | `fc65dbb` | A      | Icon loading moved into the `AssetManager`                           |
| 2026-09-20 | `29a6be9` | A      | Life icon changed from a Pac-Man to a heart                          |
| 2026-09-21 | `d6f667d` | A      | Higher-contrast title banner                                         |
| 2026-09-21 | `380bb67` | A      | `mazegenerator` vendored as a wheel file instead of a source folder  |
| 2026-09-21 | `2c46c1a` | A      | Player particles follow theme changes correctly (current HEAD)       |

## Architecture as it stands at HEAD (`2c46c1a`)

```
pac-man.py                      entry point, main loop (input -> update -> render)
config.json                     levels (size, seed, max time), validated by pydantic
src/parser.py                   pydantic Config / LevelConfig with fallback defaults
src/db_manager/user.py          users, authentication, persistent login, scores
src/logical/                    pure game logic, no pygame rendering
    maze.py                     LogicalMaze: ticks, levels, collisions, cheats
    entities.py, core_types.py  player, ghosts, states, positions
    game_event.py               GameEvent objects flushed to the visual layer
src/visual/                     scene tree (Node), Context, Draw engine, palette
    scenes/                     loading, title, game, pause, game_over, leaderboard, instructions, root
    ui/                         button, label, panel, progress, prompt, text_box
    utils/                      asset_manager, image, sprite, particle, parallax, shake, timer, font, primitives
assets/                         tiles, player, ghost, items, palettes (26), parallax, banners, fonts, icons
mazegenerator-2.1.0-*.whl       vendored maze generation library
```
