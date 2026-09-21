# Pacman - Condensed Timeline

300+ commits crunched into the changes that actually matter.
Merges, reverts of typos, and small fixes are skipped.

Authors: A = atahiri- (visual), O = obayha (logic).
Range: 2026-06-24 to 2026-09-21. Stack: Python, pygame, pydantic, numpy, uv.

## Phase 0 - Standalone building blocks (Jun 24 - Jul 4)

Utilities written before any game code existed.

| Date | Commit | By | In a nutshell |
|---|---|---|---|
| 2026-06-24 | 0b03d1f | O | Vendored the external "A-Maze-ing" maze generator package |
| 2026-07-04 | 12b5a20 | O | JSON-with-comments config parser |
| 2026-07-04 | f3803d2 | O | First users database manager |

## Phase 1 - Bootstrap and engine skeleton (Jul 5 - Jul 9)

| Date | Commit | By | In a nutshell |
|---|---|---|---|
| 2026-07-05 | 3b3228b | A | uv project bootstrap: entry point, pygame/pydantic deps |
| 2026-07-05 | 9642962 | A | Node class: scene-tree architecture for all visual objects |
| 2026-07-05 | 248cea0 | O | Maze generation plus ghost pathfinding |
| 2026-07-05 | 483e606 | A | First visual maze drawing |
| 2026-07-05 | 1a0dd0e | O | Ghost/player movement plus pac-gum positions |
| 2026-07-05 | a48b291 | A | First UI widget: button |
| 2026-07-09 | b34c239 | A | Deploy rule: export the game as a binary |

## Phase 2 - Playable gameplay core (Jul 10 - Jul 19)

| Date | Commit | By | In a nutshell |
|---|---|---|---|
| 2026-07-10 | f21d2c4 | O | Full game-logic rewrite: states, ticks, ghosts, player |
| 2026-07-10 | 4bd0636 | A | Player no longer walks through walls |
| 2026-07-10 | cb28140 | A | Real Pac-Man style movement with queued turns |
| 2026-07-10 | c2b73b1 | A | Basic player animation |
| 2026-07-11 | c9cb5f7 | A | Ghosts and pac-gums rendered on screen |
| 2026-07-12 | 1655875 | O | Player/ghost respawn events with auto-respawn delay |
| 2026-07-13 | 9232533 | A | Scene switching: title, leaderboard, game |
| 2026-07-13 | 34d5f58 | A | Pause screen |
| 2026-07-14 | 6c4dabe | O | Event rework: TickEvent enum replaced by GameEvent objects |
| 2026-07-14 | 5995181 | A | Prompt/alert widget |
| 2026-07-16 | 985381d | O | DB manager with auth system |
| 2026-07-16 | c08dbc4 | A | Visual side integrated with the new event system |
| 2026-07-16 | a3e9023 | A | feat/gameplay merged: first end-to-end playable build |
| 2026-07-16 | a28dc91 | A | Leaderboard |
| 2026-07-17 | 03690e9 | O | Multi-level support plus end-of-game handling |
| 2026-07-18 | 819adb2 | A | Score-saving form on the game-over screen |
| 2026-07-19 | 87d4aa4 | A | Persistent login plus logout |

## Phase 3 - Draw engine, sprites, assets, themes (Jul 19 - Jul 31)

| Date | Commit | By | In a nutshell |
|---|---|---|---|
| 2026-07-19 | 34a7d4f | A | Start of our own draw engine (custom rect) |
| 2026-07-19 | 7e5517e | A | Sector primitive for the Pac-Man mouth |
| 2026-07-23 | cb6e511 | A | Fully migrated to our own draw engine |
| 2026-07-24 | 34808f5 | O | Sprite logic: subsurface and flip helpers |
| 2026-07-25 | 4208664 | O | ParticleSystem with velocity/acceleration ranges |
| 2026-07-26 | dcdc177 | O | Maze rendered with tile images instead of shapes |
| 2026-07-29 | 29501c8 | A | AssetManager plus loading scene |
| 2026-07-29 | 2740bb8 | O | Numpy-based Image class for image manipulation |
| 2026-07-29 | 0bb8fab | A | Global palette with runtime theme switching |
| 2026-07-30 | 2f01bb4 | O | Parallax background |
| 2026-07-31 | 03d3b03 | A | Full palette recolor applied to the entire game |

## Phase 4 - Cheat, config, content, game feel (Aug 1 - Aug 8)

| Date | Commit | By | In a nutshell |
|---|---|---|---|
| 2026-08-01 | 5429ee5 | O | Cheat mode unlocked by a secret key combo |
| 2026-08-01 | afcc953 | A | Instructions scenes finished |
| 2026-08-04 | 01e4265 | O | Config/LevelConfig classes wired into gameplay |
| 2026-08-07 | 017bf7a | O | 10 shipped levels |
| 2026-08-07 | 8c07c44 | A | 20+ color themes |
| 2026-08-08 | f9f718a | A | Game juice: shake, hit-freeze, particles, timer |

## Phase 5 - Hardening, docs, final polish (Sep 5 - Sep 21)

| Date | Commit | By | In a nutshell |
|---|---|---|---|
| 2026-09-05 | 8980545 | A | Fixed timestep: game speed decoupled from framerate |
| 2026-09-05 | 21eb3ce | A | Game correctly ends on time-up |
| 2026-09-14 | 76c9d94 | A | Docstrings for all Python code |
| 2026-09-14 | a874802 | A | Zero flake8 errors |
| 2026-09-14 | 20f6c64 | A | Zero mypy errors |
| 2026-09-18 | 25b37c9 | A | Migrated to a home-made Vector primitive |
| 2026-09-19 | 6769a07 | A | Custom bitmap font plus PNG title banner |
| 2026-09-20 | 6b631bf | O | Collision detection fix |
| 2026-09-21 | 625e295 | A | Final README version |
| 2026-09-21 | 79fb92d | A | Vec3 moved off numpy to plain floats (last commit) |

