# Pac-Man Repository — Key Milestones Timeline

<!-- **Repo:** [`obahya/pacman`](https://github.com/obahya/pacman) · 243 total commits (condensed to milestones) -->

**Contributors:** **atahiri-** (aminedev57 — engine/UI/assets) & **obahya** (13.o.mp.3@gmail.com — core logic/maze/config/particles).

Hashes are short 7-char commit hashes; ★ = merge commit.

---

### Phase 1 — Foundation (Jun 24 → Jul 9)
- **Jun 24** `0b03d1f` ★ — obahya — First commit: external **"A-Maze-ing"** maze package
- **Jul 4** `12b5a20` `f3803d2` — obahya — JSON-with-comments parser + users **database manager**
- **Jul 5** `3b3228b` — atahiri- — Initialize **`uv` package manager** (project bootstrap)
- **Jul 5–9** `de3e726` `9642962` `a48b291` `b1783eb` `1c0aea6` — atahiri- — **Game framework scaffolding**: scene-tree `Node`/`GameComponent`, game screen, and the **button UI** element; `e2d023b` `6d7c1ef` — context object + text-based buttons
- **Jul 5** `248cea0` `1a0dd0e` ★ — obahya — First gameplay: **maze generation + ghost pathfinding**, ghost/player movement, gum positions
- **Jul 6–9** `52f2b29` `b34c239` `c08f766` `9211bf2` `c08b80a` — Build tooling: **Makefile** + binary export rule, external logger, config logging

### Phase 2 — Core gameplay & movement (Jul 10 → Jul 14)
- **Jul 10** `cb28140` `f65e317` `c2b73b1` `4bd0636` ★ — atahiri- — **Pac-Man-style movement**, persistent player movement + animation, **wall collision**
- **Jul 10** `f21d2c4` ★ — obahya — **Game logic** (collisions, gum/ghost interactions)
- **Jul 11** `c9cb5f7` `6f7e7ee` `215c582` ★ — atahiri-/obahya — **Ghosts & pac-gums on screen**; "similar movement to real Pac-Man"; ghost wall-fix; dynamic label widget; player centered spawn
- **Jul 12–13** `1655875` `ff1c7eb` `9232533` `34d5f58` — Player/ghost **respawn + events**, pause screen, basic scene change
- **Jul 14** `f60ed61` `6c4dabe` `5ee65d0` `4cf03b5` `5995181` `19d7dc9` ★ — obahya/atahiri- — **New event system** (`GameEvent`), prompt/alert widget, progress bar, centered maze

### Phase 3 — UI polish, auth & leaderboard (Jul 15 → Jul 18)
- **Jul 15–16** `1a27ec2` `a28dc91` `c12fb03` `1216167` `5900a49` `08493f4` ★ — atahiri- — Level progress bar, **leaderboard**, panel, textbox, game-over screen
- **Jul 16** `985381d` `6098a72` — obahya — **DB manager with authentication** + auto-login
- **Jul 17–18** `4bed19c` `03690e9` `819adb2` `8e58247` `87d4aa4` ★ — **End-of-game handling** (`WinEvent`), level arguments, score-save form, **persistent login/logout**; `ce1a02a` ★ — `feat/ui` **merged into main**

### Phase 4 — Custom draw engine (Jul 19 → Jul 23)
- **Jul 19–23** `34a7d4f` `7e5517e` `aed697f` `24574ce` `297567c` `918de00` `cb6e511` ★ — atahiri- — **Replaced pygame drawing with a custom engine**: custom rect/round-rect/circle functions, border thickness; `ec926a5` ★, `d3b5a54` ★ — merged into mainline
- **Jul 20–23** `004afd4` `6d5f5f6` `d8532f2` ★ — **Level-up mechanic**, game-won screen; `5d23a37` `2cec83a` — obahya/atahiri- — **pre-computed ghost next-move** (pathfinding optimization)
- **Jul 24–28** `bd14e69` `34808f5` `916c133` `7c84b85` `2740bb8` ★ — **Sprite type** + `subsurface`/`flip_surface`; numpy added; obahya's **Image class**; `29501c8` `878df66` `2142652` — asset manager, ghost/player sprites

### Phase 5 — Particles, tilesets, transparency (Jul 25 → Jul 27)
- **Jul 25** `4208664` ★ — obahya — **`ParticleSystem`** (single surface, velocity/acceleration)
- **Jul 25–27** `79defeb` `4f4f371` `fb9f4ff` `c5b0cf0` `892f149` ★ — atahiri- — **Draw-engine transparency**, tileset assets, **walking particles** for the player
- **Jul 26** `dcdc177` ★ — obahya — **Draw the maze using images**; `9ec54ac` ★ `f39c700` `9780f6f` — atahiri- — new game-screen UI

### Phase 6 — Theming & parallax (Jul 28 → Aug 6)
- **Jul 29–31** `0bb8fab` `8f6361d` `5dc7741` `03d3b03` `af5620e` ★ — atahiri- + obahya — **Global palette & dynamic theme switching**; `6f15677` — rgb-tuple color refactor
- **Jul 30** `2f01bb4` ★ — obahya — **Parallax background**; `c15b2ec` `744eb65` `90e2d1d` — palette switching, alpha-safe fill
- **Aug 5–6** `c3f88be` `f5ac938` `486ebfa` ★ — atahiri- — parallax layers, dim/slow during gameplay, persistence fix

### Phase 7 — Instructions, cheat mode, config (Aug 1 → Aug 5, obahya-heavy)
- **Aug 1** `5429ee5` ★ — obahya — **Cheat mode** via key combination; `d3e4285` — **hashed** the cheat code
- **Jul 31–Aug 1** `f606ff8` `c962a72` `afcc953` ★ — atahiri- — **Three-page instructions screen**; `5be8880` `e8ce736` — blueprint + instructions button
- **Aug 2–5** `01e4265` `69ac88d` `d6c3da0` `a7bcf86` `a85ad40` `4e7261b` ★ — obahya — **Config system overhaul** (`Config`/`LevelConfig`, level speed, lives), `LogicalMaze` refactor, level-end detection
- **Aug 3** `60fc0d6` `75f52a0` `1997943` `e8942bd` ★ — **Full docstring pass** across visual/module code (`feat/docs`)

### Phase 8 — Game juice & final polish (Aug 4 → Aug 8, current HEAD)
- **Aug 4** `baa72d2` `38b8c78` — obahya — `ParticleSystem` play/stop, ghost movement update
- **Aug 4–5** `b6b3284` `202b883` `75c832a` `81345d3` `7c860b7` ★ — atahiri- — **Dynamic UI on level change**, level-change visual fixes, winning instruction
- **Aug 6–7** `375ea21` `8c07c44` **`f1e1dec`** — atahiri- — **20+ themes**, theme-change button, `a536521` — separate title font
- **Aug 7–8** `46a6123` `142c260` `d528cdf` `187a0e1` `f9f718a` ★ — atahiri- — **"Game juice"**: shake utility, timer component, freeze-on-eating-ghost **`(HEAD commit)`**

---

### Noteworthy milestones (quick view)
| Date | Commit | What |
|------|--------|------|
| Jun 24 | `0b03d1f` | First commit — A-Maze-ing package |
| Jul 5 | `3b3228b` | uv project bootstrap |
| Jul 10 | `cb28140` / `f21d2c4` | Real movement + game logic |
| Jul 16 | `985381d` | Auth & leaderboard |
| Jul 23 | `cb6e511` | Custom draw engine |
| Jul 30 | `2f01bb4` | Parallax background |
| Aug 1 | `5429ee5` | Cheat mode |
| Aug 7 | `8c07c44` | 20+ themes |
| Aug 8 | `f9f718a` | Game juice (HEAD) |

