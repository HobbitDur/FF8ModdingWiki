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

**The naive gate flickers.** Simply skipping the tick on 3 of 4 frames gives correct *speed*
but **flickers**: the effect **draws inside its update tick** —
`InitEffectSequenceFromData` (0x571C80) rebuilds the effect's geometry into the battle render
list every frame; there is no separate render pass — so a skipped tick drops the effect's
geometry that frame.

**Working fix — frame-hold (snapshot-restore).** Run the tick **every** frame (so it always
draws), but on 3 of 4 frames **snapshot a memory window around the effect's root pointer**
before the tick and **restore it after** — undoing the state advance while keeping the draw.
The effect advances at 15 fps yet is drawn every frame → correct speed, **no flicker**.
(Window used: `effect_ctx − 0x2000`, size `0x8000`; each spell's pools cluster around the root
`C3_28_GF_data_pointer` the tick receives.)

**Only hold genuine magic casts.** The tick is shared. Draw/Stock rides the same effect tick,
but its handler writes external state the window-restore can't undo → a **delayed crash**.
Discriminate on the battle command type `BattleTask68Data.commandTypeWIthGunblade`
(byte +1 of `*BATTLE_TASK_68_DATA_ADDR` @0x1D99A50), verified in-game:

| commandTypeWIthGunblade | Action | Frame-hold? |
|---|---|---|
| 0x02 | Magic cast | **Yes** |
| 0x06 | Draw / Stock | No — restore corrupts state (crash) |
| 0x26 / 0xF4 / 0xFE | GF summon cinematic | Not this way — skeletal model, see [GF Summon Runtime](../gf-summon-runtime/) |
| 0x00 | Physical attack | No |

Capture the holdable effect-queue pointer only when the magic-cast handlers
(`BattleActionSequence_Tick_MagicCast` 0x50A9A0 / `_MagicEffect` 0x50B190) register it under
cmd 0x02; hold the tick only when `effect_ctx` equals that captured pointer.

**Side effects re-fire on held frames** (the tick re-runs), so suppress them while holding via
a flag:

| Side effect | Function | Held-frame action |
|---|---|---|
| Effect SFX | `PlayWorldSound` (0x46B2A0) | no-op → plays once |
| Damage/heal number | `BattleFx_DamageNumbers_Spawn` (0x5068B0) | no-op → shows once |

Damage itself is applied once (externally guarded), so only the *display* duplicated.

### Implementation (FFNx, 2013 EN exe)

**Hext does not work here.** The 2013 DotEmu wrapper refuses to execute new code written into
`.text` padding (a gate stub in the `0xB68940` cave crashes), and packed `.text` has no room
to inline the gate. In-place edits to *existing* code do work (verified: NOP-ing the tick call
at `0x50093A` froze the effect cleanly), but there is no cave to host the counter logic.

So the gate lives in a custom **FFNx** build (shipped as `AF3DN.P`): `replace_call(0x50093A,
gate)` for the frame-hold, plus `replace_function` hooks on the cast handlers (to capture the
holdable pointer under cmd 0x02) and on the SFX / damage-number functions (to de-dupe).
Confirmed in-game: **single-target magic at true 60 fps** — correct speed, no flicker, single
SFX, single damage number, and Draw/Stock no longer crashes.

## IDB names applied

Functions (FF8_EN.exe): `MAG_102_THUNDARA_Init` (0x6DC2E0), `_Tick` (0x6DC390),
`_BoltTask` (0x6DC510); `MagicEffect05_*` tree (0x8D4430–0x8D4BA0);
`BattleTask68_DispatchActionSequence` (0x50A790, action-seq handler by command type);
`BattleActionSequence_Tick_MagicCast` (0x50A9A0, full magic cast — Firaga),
`BattleActionSequence_Tick_MagicCast_NoTarget` (0x50BC20),
`BattleActionSequence_Tick_GF_Cinematic` (0x50B2A0), `_MagicEffect` (0x50B190);
`Magic_GetIDLoad` (0x50AF20); `BattleFx_DamageNumbers_Spawn` (0x5068B0),
`BattleFx_DamageNumbers_TaskTick` (0x5069B0).

Globals: `C3_28_GF_data_pointer` (0x1D96AAC, effect-tick root), `BATTLE_TASK_68_DATA_ADDR`
(0x1D99A50, ptr to `BattleTask68Data`), `MagicList_Logic` (0xC81774) /
`MagicList_TextureLoad` (0xC81DB8, fn-ptr arrays indexed by effect_id−1),
`MAGIC_EFFECT_LOGIC_CALLBACK` (0x21DFEC4), `MAGIC_EFFECT_LOGIC_CALLBACK_2` (0x21DFEC0).

### Open

- Exact runtime use of the kernel +0x06 category byte (does effect 5 actually play for
  offensive spells, and when?).
- Multi-target magic under the frame-hold (only single-target verified in-game so far).
- Thundara bolt palette/CLUT source (element colour).
