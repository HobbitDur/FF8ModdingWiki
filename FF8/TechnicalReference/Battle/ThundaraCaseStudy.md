---
layout: default
parent: Battle
title: "Case study: Thundara animation"
permalink: /technical-reference/battle/thundara-case-study/
---

The fifth worked spell animation — **Thundara** (effect_id 102, `mag101.tim`) — after
[Firaga](../firaga-case-study/), [Cure](../cure-case-study/), [Fire](../fire-case-study/) and
[Blizzard](../blizzard-case-study/).

Thundara was picked for a specific reason: it is a **thunk**, the largest unclassified group in the
[magic effect census](../../list/magic-effect-census/) (111 of 345 slots). Reading it answers what
that group actually is — and the answer is *nothing*: a thunk is a forwarder, not a family (§1).
Behind the forwarder, Thundara is an ordinary **timeline** effect, the same archetype as Fire and
Blizzard.

Its own contributions are three:

- **the effect iterates ACTIONS, not targets** — the opposite of Fire, and it corrects a
  long-standing note in our own analysis (§3);
- **a re-strike lockout** — a 3-slot scan that refuses to bolt a target whose previous bolt has not
  yet dealt its damage (§4);
- **the "lightning strobe" was never a strobe** — it is a double-buffered packet arena, and the
  earlier claim that it caused the flicker was wrong (§7).

Addresses are `FF8_EN.exe`; everything below is named, typed and commented in the IDB.

1. TOC
{:toc}

## 1. The thunk is not an archetype

The census keyed 111 slots as a "thunk" family because their dispatch-table entry points at a
14-byte function. Reading one shows why that was a category error:

```c
TaskQueueHeader *__cdecl MAG_102_THUNDARA(int cast_context) {          // 0x6DC2D0, the dispatched fn
    return (TaskQueueHeader *)MAG_102_THUNDARA_Init(cast_context);     // 0x6DC2E0, the real effect
}
```

That is a calling-convention adapter: it casts and tail-calls. The 14 bytes are the size of the
*forwarder*, and say nothing about the effect behind it. The archetype is whatever the target is,
and resolving it is mechanical (`get_callees`) — though the thunk→target offset varies (+0x10 for
Thundara and Thunder, +0x30 for Diablos, +0xF0 for Quezacotl), so it cannot be done by fixed
arithmetic.

**Thundara's target is a plain timeline effect.** One data point does not classify the other 110,
but it does retire the idea that they share a family.

## 2. Structure

`MAG_102_THUNDARA_Init` (0x6DC2E0) sets up **four pools across two queue pairs** — more than Fire
(one pool) or Blizzard (one pool), because Thundara's particles have three distinct lifetimes:

| Pool | Node size × count | Content |
|---|---|---|
| `MAG102_THUNDARA_directorPool` | 0x14 × 1 | the root director (`_Tick`) |
| `MAG102_THUNDARA_boltPool` | 0x6C × 3 | the bolts — **max 3 concurrent** |
| `MAG102_THUNDARA_sparkPool` | 0x2C × 60 | ground sparks (20 per bolt × 3) |
| `MAG102_THUNDARA_flashPool` | 0x18 × 32 | secondary flashes |

The 3/60 relationship is not a coincidence: 3 bolts × 20 sparks = 60, so the pools are sized to let
every concurrent bolt own a full spark ring. On cast it also fires the keyframe camera track
`MAG102_THUNDARA_cameraAnim` and queues the TIM upload.

## 3. The director iterates ACTIONS, not targets

`MAG_102_THUNDARA_Tick` (0x6DC390), once per 15-frame cycle:

```c
action_data = MAG102_THUNDARA_castCtx->action_data;
if ( director->action_index <= action_data->actionCountMinus1 )        // <-- element 0's count
    ... action_data[director->action_index].targetData->TargetSlotId   // <-- action i's FIRST target
```

This is worth stating plainly because it is the reverse of Fire, and because the raw pseudocode
hides it. `sizeof(BattleActionTaskData) == 20`, so before the struct was applied this read as
`*(v2 + 20*i + 8)` and `*(v2 + 17)` — and an earlier note in our own analysis recorded `+17` as
"target count" on that basis. It is not:

| | Fire | Thundara |
|---|---|---|
| loop over | `targetData[0 .. target_count-1]` | `action_data[0 .. actionCountMinus1]` |
| stride | 24 (`FF8BattleTargetData`) | 20 (`BattleActionTaskData`) |
| bound field | `action_data[0].target_count` (+16) | `action_data[0].actionCountMinus1` (+17) |
| targets used | all of one action's | only `targetData[0]` of each action |

Both fields are real and adjacent, which is exactly why they were confusable. Element 0 carries the
counts for the whole sequence; `+16` counts the targets of an action, `+17` counts the actions.

**Esuna (24) corroborates this independently.** `MAG_024_ESUNA_Init` (0x88CF70) reads *both* fields
and takes their minimum:

```c
HIWORD(node[7].next) = *(action_data + 16);        // target_count
LOWORD(v3)           = *(action_data + 17);        // actionCountMinus1
HIBYTE(node[3].task_func) = min(target_count - 1, actionCountMinus1);
```

A `min()` of the two is only meaningful if they are different quantities. No effect that treated
`+17` as "target count" could produce this code.

The practical consequence: **a multi-hit Thundara fires one bolt per hit, sequentially**, and a
multi-*target* Thundara only works because the engine builds one action per target. Thundara never
reads `targetData[1]`.

## 4. The re-strike lockout

Before spawning, the director scans all three bolt slots. The loop *continues* while a slot is
free, or holds a bolt on a different target, or holds a bolt older than 26 frames. It therefore
**exits early — skipping the spawn — when a bolt is already active on this action's target and is
younger than 26 frames.**

26 is not arbitrary: **26 is the frame the bolt applies damage** (§5). The lockout is precisely
*"do not re-strike a target until its previous bolt has landed its hit."* The action is not
dropped — `action_index` simply is not advanced, so the same action is retried on the next
15-frame cycle.

This is the third distinct solution to the same problem across the case studies: Fire uses a slot
mutex, Blizzard pipelines its directors 28 frames apart with no interlock at all, and Thundara
scans its live pool. There is no shared mechanism — each effect's author solved it locally.

> One wrinkle for readers of the pseudocode: the early-exit path stores `director->frame_cycle = 0`,
> which is **dead** — the enclosing branch only runs when `frame_cycle` is already 0. It does not
> cause an immediate retry.

## 5. The bolt — a 32-frame timeline

`MAG_102_THUNDARA_BoltTask` (0x6DC510). Spawn position is bone `0xF1` of the target entity.

| Frame | Event |
|---|---|
| 0 | spawn the **20-spark ground ring** (§6) |
| 4 | `BdPlaySE3D` — the thunder crack |
| 11–31 | the **strike render block** (12 layers, below) |
| 12 | **blast the sparks outward**; screen flash |
| 23 | screen flash |
| 15–30 (even) | 2 **secondary flashes** per even frame at a random point on a ~300-radius ring |
| 26 | **`ApplyActionResultToTarget`** — damage |
| 31 | die |

Note the sparks precede the bolt by 11 frames: the ground crackles and brightens *first*, then the
bolt strikes into it. The damage lands at 26, well after the visual peak.

### The strike render block

The render block runs on `v15 = frame − 11` and composites **twelve overlapping layers** — nine
keyframed sprite sequences and three GTE prim models — each with its own window:

| Window (`v15`) | Layer |
|---|---|
| 0–7 | `boltLayer_core_f0` — the bolt itself |
| 2–9 | `boltLayer_high_f2` (drawn 200 above), `boltLayer_mid_f2` |
| 2–10 | `boltLayer_ground_f2` |
| 1–12 | `RenderTiltedGlow(+512)` — prim model, tilted |
| 0–11 | `RenderColumn` — prim model, **anisotropic** scale (tall: `2·sin` in Y vs `sin/4+512` in X/Z) |
| 5–13 | `boltLayer_burst_f5` |
| 5–12 | `boltLayer_highBurst_f5` (200 above) |
| 3–14 | `RenderTiltedGlow(−512)` — the mirrored tilt |
| 4–19 | `RenderFlashBall` — prim model, **uniform** `sin` scale (expands then collapses) |
| 8–16 | `boltLayer_afterglow_f8` |
| 11–19 | `boltLayer_fade_f11` |
| 9–18 | `boltLayer_pulsing_f9` — RGB modulated by `0x80 − sin(((v15−9)<<10)/10)>>7` |

The two `RenderTiltedGlow` calls at `+512` and `−512` are the same model drawn at mirrored tilts —
a cheap way to fake a forked bolt. All three prim models go through `Effect_RenderPrimModel` with
blend mode 243.

The screen flash (`MAG_003_sub_7011A0`) is **Thunder's** routine, not Thundara's: the tiers share
this helper even though they are otherwise separate effects.

## 6. The sparks — rise, then blast

`MAG_102_THUNDARA_Spark_Tick` (0x6DCC00) is a textbook velocity/acceleration integrator, fully
readable now that `TaskNodeThundaraSpark` is applied:

```c
spark->vel_x += spark->accel_x;   ...
spark->pos.posX += spark->vel_x >> 4;   ...
spark->rgb_level += spark->rgb_delta;    // clamped to [0, 128]
```

Twenty are spawned at bolt frame 0 on a ring of radius `(target.size >> 1) + 200`, at `bolt.y + 500`
— i.e. **on the ground**, since [+Y is down](../blizzard-case-study/#5-the-y-axis-settled). Each gets:

| Field | Value | Meaning |
|---|---|---|
| `vel_y` | `−512 − (rand & 0x3FF)` | **upward** (−Y is up) |
| `accel_y` | `−vel_y >> 4` = +32..+95 | gravity, pulling it back down |
| `rgb_delta` | `+24 .. +39` | **brightening** — the charge-up |
| `start_delay` | `rand & 7` | staggered start |
| `anim_phase` | `rand` | de-synced sprite phase (`% 20`) |

At bolt frame 12 — one frame after the strike becomes visible — all twenty are **re-aimed**:

```
vel   = 16 × (spark.pos − bolt.pos)   horizontally;  vel_y = 0
accel = vel / −10                      (deceleration)
rgb_delta = −10 − (rand & 7)           (now fading)
```

Setting velocity proportional to the *existing* offset from the bolt makes the ring explode outward
with its shape preserved and the farthest sparks moving fastest — a radial blast for four
multiplies, no trig, no per-spark direction stored.

## 7. The packet arena is not a strobe

Each frame the director resets a cursor to one of two 32 KB arenas:

```c
if ( director->packet_arena_parity ) { packetCursor = packetArenaBase; ...parity = 0; }
else                                 { packetCursor = packetArenaBase + 0x8000; ...parity = 1; }
```

An earlier note recorded this as *"flickers by toggling the texture VRAM page each frame — the
lightning strobe."* **That was wrong.** `packetCursor` is a **bump allocator**: every
`InitEffectSequenceFromData` call takes it as the output buffer and returns the advanced cursor,
and the whole 12-layer render block threads it. Alternating per frame is ordinary
**double-buffering** — the same `vramEven`/`vramOdd` scheme as [Cure](../cure-case-study/) — so the
GPU can read last frame's packets while this frame's are built. It is invisible.

The visible flicker comes from the layer windows in §5 overlapping and expiring, not from this.
The correction matters for the 60 fps work: a genuine per-frame strobe would strobe 4× faster and
need gating, whereas a double-buffer needs nothing.

## 8. 60 fps analysis

Thundara is frame-counter driven throughout and quarter-scales like Fire and Blizzard:

- **counters ×4**: the director's 15-frame cycle, the bolt's 32-frame life, damage at 26, the
  lockout's 26, the spark's 32-frame life and `start_delay`, and every window in §5. These are all
  hardcoded immediates, so this is a code change, not a data change.
- **dynamics ÷4**: the spark integrator is `vel += accel; pos += vel >> 4` — accelerations quarter
  and the shift absorbs the rest, near-losslessly, as in Fire.
- **the lockout's 26 must scale with the damage frame's 26** — they are the same quantity written
  twice, in two different functions. Scaling one and not the other would let a target be re-struck
  before its damage lands.
- **`RenderFlashBall` / `RenderColumn` / `RenderTiltedGlow` are already parametric** in
  `(frame, duration)` — they compute `sin((a3 << 10) / a4)`, so passing the ×4 duration makes them
  interpolate for free. This is the one part of Thundara that is smooth at 60 fps with no extra work.
- the camera track is keyframe data and is interpolatable, as everywhere else.
- the packet arena parity needs **no** change (§7).

## 9. Function reference

| Address | Name | Role |
|---|---|---|
| 0x6DC2D0 | `MAG_102_THUNDARA` | the dispatched **thunk** — forwards to `_Init` |
| 0x6DC2E0 | `MAG_102_THUNDARA_Init` | 4 pools, camera, TIM upload, first director |
| 0x6DC390 | `MAG_102_THUNDARA_Tick` | director: 15-frame cycle, per-action loop, lockout |
| 0x6DC510 | `MAG_102_THUNDARA_BoltTask` | 32-frame bolt: 12 render layers, damage at 26 |
| 0x6DCC00 | `MAG_102_THUNDARA_Spark_Tick` | spark integrator (rise → blast → fade) |
| 0x6DCD10 | `MAG_102_THUNDARA_Flash_Tick` | 8-frame secondary flash sprite |
| 0x6DCD90 | `MAG_102_THUNDARA_RenderTiltedGlow` | prim model, tilt from arg (±512) |
| 0x6DCE80 | `MAG_102_THUNDARA_BuildTiltMatrix` | its rotation matrix |
| 0x6DCEE0 | `MAG_102_THUNDARA_RenderColumn` | prim model, anisotropic (tall) `sin` scale |
| 0x6DCFE0 | `MAG_102_THUNDARA_RenderFlashBall` | prim model, uniform `sin` scale |
| 0x7011A0 | `MAG_003_sub_7011A0` | screen flash — **shared with Thunder** |

Structs: `TaskNodeThundaraDirector` (20 B), `TaskNodeThundaraBolt` (108 B — pos + 20 spark
pointers at +28..+107), `TaskNodeThundaraSpark` (44 B), `TaskNodeThundaraFlash` (24 B).

Data: `MAG102_THUNDARA_cameraAnim` (0x1321588), `boltSoundId` (0x1321BD8), `screenFlashParam`
(0x1321BDC), `tiltedGlowModel` (0x13200D0), `columnModel` (0x13207B8), `flashBallModel`
(0x1320EA0), plus the nine `boltLayer_*` / `sparkSeq` / `flashSeq` sprite sequences (0x131E760–
0x131FF74).

## 10. Open questions

- **The nine sprite-sequence layers are named by their frame windows, not by their art.** Their
  roles (`core`, `high`, `ground`, `burst`, `afterglow`, `fade`, `pulsing`) are inferred from draw
  order, offsets and blend, not from decoding `mag101.tim`. Rendering the atlas would confirm or
  correct them.
- **The bolt-pool scan is documented by comment, not by type.** The compiler biased the scan pointer
  +12 (so Hex-Rays prints `v5[-1].sparks[17]` for `boltPool[i].header.flags_and_priority`); the bias
  is not expressible as a struct, so the loop carries an explanatory comment instead.
- **`target_entity[3].sequence_id` (entity +38)** is used as the spark-ring radius basis
  (`(x >> 1) + 200`) and the flash-ring basis (`+300`). It is presumably a size/height field on
  `FF8BattleEntitySlotData`, but it was typed by usage here, not decoded.
- **The other 110 thunks are now resolved** — all timeline, see the
  [census](../../list/magic-effect-census/). But only Thundara has been *read*; the rest are
  classified by init shape. Thunder (3), Blizzara (103), Blizzaga (104) and Thundaga (105) are the
  natural next reads — `MAG_103_BLIZZARA_Init` is structurally identical to Thundara's init, and
  Thundaga's `_Tick` (0x6D3E50) is already known to run a 46-frame master cycle.
