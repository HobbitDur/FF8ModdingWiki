---
layout: default
parent: Battle
title: Magic Spell Effect Runtime
permalink: /technical-reference/battle/magic-spell-effect-runtime/
---

How a **regular magic spell** (Fire, Thunder, Thundara, …) resolves to its on-screen effect,
which mag file it uses, and why the effect is largely **procedural code** rather than
keyframe data — the key constraint for 60 fps work. Complements
[GF Summon Runtime](../gf-summon-runtime/) (GF cinematics).

1. TOC
{:toc}

## Resolution chain (worked example: Thundara)

The per-spell effect is selected by the kernel magic entry field at **+0x04** (labelled
"Magic ID" on the [kernel magic page](../../main/kernel/magic/), but it is really the
**effect id**). It is copied into the battle action task at **+6** and dispatched:

```
Thundara ── kernel magic entry @0x03FC ──▶ field +0x04 (effect_id) = 102
                                                    │  (copied to action task +6)
        Magic_GetIDLoad(effect_id) @0x50AF20  ──▶  idx = 102 - 1 = 101
                                                    │
                    MagicList_Logic[101] = 0x6DC2D0  = MAG_102_THUNDARA
                    MagicList_TextureLoad[101] = 0x6DC2B0  → loads mag101.tim
```

Rule (from the Shiva work): **mag file number = effect_id − 1**. Thundara → effect_id 102 →
**mag101**. IDB functions follow the scheme `MAG_<effect_id>_<NAME>`.

> Do not confuse the two "+6"s: the **action task** offset +6 holds the effect_id, and it is
> sourced from the kernel entry field **+0x04** — *not* from the kernel byte at +0x06.

### Elemental spell → effect_id → file

Verified from `kernel.bin` (+0x04) and the IDB function names:

| Spell | kernel +0x04 | effect_id | Handler | File |
|-------|--------------|-----------|---------|------|
| Fire | 2 | 2 | `MAG_002_FIRE` (0x6298A0) | mag001 |
| Thunder | 3 | 3 | `MAG_003_THUNDER` (0x700C10) | mag002 |
| Thundara | 102 | 102 | `MAG_102_THUNDARA` (0x6DC2D0) | mag101 |
| Thundaga | 105 | 105 | `MAG_105_THUNDAGA` (0x6D3DB0) | mag104 |

Note the three thunder tiers use **different** effects (bigger spell → bigger effect), so
tiers do **not** share a file.

## The kernel "+0x06 Animation triggered" byte is NOT the selector

Dumping the +0x06 byte for every spell family gives only two values — `5` for **all**
offensive spells, `0` for **all** curatives. It is a coarse category flag, not a per-spell
id. Its exact runtime role is unconfirmed; it routes to a shared/secondary effect
(`effect_id 5`, handler `0x8D4450`, loads `mag004_034.tim`, previously mis-guessed
`MAG_005_PHOENIX_DOWN`), which is **not** the per-spell animation. Renamed in the IDB to a
neutral `MagicEffect05_*` scheme:

| Address | Name | Role |
|---------|------|------|
| `0x8D4450` / `0x8D4430` | `MagicEffect05_Init` / `_LoadTexture` | Shared effect entry + `mag004_034.tim` load |
| `0x8D4530` | `MagicEffect05_Tick` | Procedural particle engine (state machine + 4 particle queues) |
| `0x8D4640` / `0x8D4A10` / `0x8D4BA0` | `_Emitter_Tick` / `_SpawnSparkParticles` / `_Particle_Tick` | Element-agnostic particle spawners (hardcoded sprite templates) |

## The real Thundara effect (effect_id 102)

`MAG_102_THUNDARA` (0x6DC2D0) → body `MAG_102_THUNDARA_Init` (0x6DC2E0):

- Loads **mag101.tim**, allocates particle task-queues (pools 3 / 60 / 32).
- Fires a **keyframe camera animation** `Battle_PlayCameraAnimation(&unk_1321588)` — the
  strike swoop.
- Tick `MAG_102_THUNDARA_Tick` (0x6DC390):
  - Iterates the attack's **target list** (from the action ctx: +17 = target count,
    +8+20·i = per-target slot) and spawns a **bolt task per target**
    (`MAG_102_THUNDARA_BoltTask`, 0x6DC510).
  - **Flickers** by toggling the texture VRAM page each frame (`dword_2544360` vs
    `+0x8000`) — the lightning strobe.
  - Timed by a **frame-cycle counter** (`a1[1].flags_and_priority`, wraps at 15) and a
    per-frame target step — all **frame-counter driven**, not keyframed.

## Timing model — why 60 fps breaks spell effects

Battle logic runs at ~15 fps in vanilla; an uncap to 60 fps ticks it **4×**. Spell effects
carry their own **frame counters incremented once per tick** and compare them against
**hardcoded frame constants** (e.g. Thundara's 15-frame bolt cycle; the shared
`MagicEffect05` spark window `[21,36]`). At 4× tick rate every effect resolves in ¼ the
time, particles spawn 4× as dense, and SFX fire early.

### Implication for the 60 fps mod

| Content | Mechanism | 60 fps fix |
|---------|-----------|------------|
| Model motion (character / monster / GF) | skeletal keyframes + frame-count header | interpolate: insert tweens, ×4 count field (**data**) |
| **Battle/effect camera** (e.g. Thundara `unk_1321588`) | keyframe camera track | interpolate (**data**) |
| **Spell particle effects** (`MAG_*` handlers, shared `MagicEffect05`) | procedural, per-tick frame counters + hardcoded constants + `rand()` | **code**: gate the effect ticks to advance every 4th frame, or ×4 every counter/constant |

Cleanest route for spell particles: **gate the effect tick functions (and the shared
particle-task update) to step once per 4 rendered frames** — run effect logic at 15 fps
under a 60 fps render loop. The camera tracks can be interpolated as data.

## The single per-frame driver — one gate fixes every effect

Every active magic/GF effect is a task tree whose **root queue** is stored in the global
`C3_28_GF_data_pointer` (0x1D96AAC), set by the effect's Init (e.g. `MAG_105_THUNDAGA_Init`
returns `&stru_2543DD0.data`). The whole tree is ticked **once per battle frame** from a
single line in the battle frame-update `BdLink_GF_battle_input_and_texture_upload` (0x500900):

```c
// @0x50093A — ticks the ENTIRE active spell/GF effect once per frame
if ( C3_28_GF_data_pointer && !ExecuteTaskQueue(C3_28_GF_data_pointer) )
    C3_28_GF_data_pointer = 0;      // effect finished -> clear
```

Because the whole battle update runs 4× under a 60 fps uncap, this line runs 4× → every
spell/GF effect plays 4× too fast.

**Fix (one patch, all effects):** execute this `ExecuteTaskQueue` only **every 4th frame**
(skip on 3 of 4; do not clear the pointer on skipped frames). The effect then advances at
its native 15 fps → correct duration, spawn density, and synced SFX — for **all** spells and
GFs, with no per-effect work and no constant rescaling.

Model/character animations are driven by the **other** `ExecuteTaskQueue` calls in the same
function (`battle_tasks_init_*`), so they are untouched by this gate and can be smoothed
separately via data interpolation.

### Implementation (Hext, 2013 EN exe)

The gate is a 5-byte redirect of the effect-tick call (VA `0x50093A`) to a 25-byte stub in
`.text` padding (VA `0xB68940`) that runs the real `ExecuteTaskQueue` only every 4th frame,
using a counter in `.data` (VA `0x188B100`). Skipped frames return the (non-zero) queue
pointer so the effect freezes instead of ending. File offsets = VA − 0x400000 (flat map).

```
10093A  = E8 01 80 66 00                                             ; call stub (rel32 0x668001)
768940  = FF 05 00 B1 88 01 A1 00 B1 88 01 A8 03 74 05 8B 44 24 04 C3 E9 C7 FA 9F FF
148B100 = 00 00 00 00                                                ; frame counter
```

To gate for a ×2 uncap instead of ×4, change `A8 03` (test al,3) to `A8 01` (test al,1).

## IDB names applied

Functions (FF8_EN.exe): `MAG_102_THUNDARA_Init` (0x6DC2E0), `_Tick` (0x6DC390),
`_BoltTask` (0x6DC510); `MagicEffect05_*` tree (0x8D4430–0x8D4BA0);
`BattleActionSequence_Tick_GF_Cinematic` (0x50B2A0), `_MagicEffect` (0x50B190).

Globals: `MAGIC_EFFECT_LOGIC_CALLBACK` (0x21DFEC4), `MAGIC_EFFECT_LOGIC_CALLBACK_2`
(0x21DFEC0), `MAGICEFFECT05_TEX_FILEHANDLE` (0x27618A0), `MAGICEFFECT05_TEX_VRAM_A/B`
(0x276C294 / 0x276C290).

### Open

- Exact runtime use of the kernel +0x06 category byte (does effect 5 actually play for
  offensive spells, and when?).
- `0x50BC20` dispatcher category (uses callback slot 2; item?).
- Thundara bolt palette/CLUT source (element colour).
