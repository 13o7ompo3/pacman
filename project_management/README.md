# Project Management

## The initial split

We are two people: atahiri- and obahya. At the start we split the
project in two halves that could grow in parallel:

- obahya owned the logic: maze generation, game rules, events,
  config parsing, and the users database.
- atahiri- owned the visual: scene tree, draw engine, UI widgets,
  scenes, assets, and themes.

The contract between the two halves was small on purpose: a logical
maze object plus a GameEvent queue. That let us test early without
stepping on each other's code, each on our own feat branches merged
back into main.

## How it evolved

Week 1 was skeleton work: project bootstrap, the Node scene tree,
and the first maze on screen. Once both halves existed, we
integrated them into the first playable build (mid-July) and never
looked back.

From there the plan bent in three ways:

1. We built our own engine instead of leaning on pygame drawing.
   The custom draw engine, sprites, particles, and AssetManager
   took more time than planned but made themes and effects easy.
2. Polish became a feature. Themes, parallax, screen shake,
   hit-freeze, and cheat mode started as extras and became core
   to how the game feels.
3. We paid down quality debt at the end. The last stretch was
   config-driven levels, a fixed timestep, full docstrings, and
   zero flake8/mypy errors before the final README.

## In short

We planned logic vs visual, integrated early through a thin event
interface, then let the visual side pull us toward juice and themes
while the logic side hardened rules, config, and collisions.

