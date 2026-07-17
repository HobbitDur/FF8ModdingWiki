---
layout: default
parent: Battle
title: "Case study: Fire animation"
permalink: /technical-reference/battle/fire-case-study/
---

The third worked spell animation — **Fire** (effect_id 2, `mag001.tim`) — alongside
[Firaga](../firaga-case-study/) and [Cure](../cure-case-study/). Fire is the **timeline archetype
in its simplest form** (a 22-frame director, everything at hardcoded frame numbers), and it
demonstrates four patterns the other two case studies don't have:

- **target-count dispatch** — separate single-target and multi-target directors, chosen per action;
- **pipelined multi-hit** — chained directors 12 frames apart, serialised per target by a
  **slot mutex**, instead of Cure's strictly sequential loop;
- **a shared, palette-recoloured sprite** — the spark artwork is not Fire's; it is recoloured to
  the fire palette through the CLUT-row mechanism of the
  [sprite sequence format](../cure-case-study/#the-sprite-sequences);
- **the ground light pool** — a flat quad under each flame whose brightness tracks the flame's
  height.

Addresses are `FF8_EN.exe`. All functions below are named and commented in the IDB.

1. TOC
{:toc}

## 1. Init and the pools

`MAG_002_FIRE_Init` (0x6298A0) sets up just **two** pools — contrast Cure's four:

| Pool | Node size × count | Role |
|---|---|---|
| root | 0x10 × 1 | `MAG_002_FIRE_RootTask` (header-only — no payload) |
| `MAG002_FIRE_particlePool` | 0x24 × 150 | **everything else**: directors, flames, embers, sparks |

It resets the 7-entry per-slot mutex `MAG002_FIRE_slotFree` to all-free, plays
`MAG002_FIRE_cameraAnim`, uploads the TIM, and spawns the first director — **single-target if this
action has ≤ 1 target** (the slot id stored in the node), else multi-target. The root task flips
`MAG002_FIRE_pktCursor` between two packet buffers by frame parity (the same VRAM double-buffer
trick as Cure's `activeVram`) and ends the effect when the particle queue drains.

## 2. The directors — a 22-frame timeline

One director per action/hit, node `TaskNodeFireDirector` (36 bytes). The whole spell is a fixed
timeline:

| Frame | Single-target | Multi-target |
|---|---|---|
| 0 | **claim the slot mutex** (waits while `slotFree[slot] == 0`) | — |
| 1 | spawn **4 flames** on the target | spawn **1 flame per target** |
| 6 | `BdPlaySE3D` at the target | `BdPlaySE` (flat) |
| 8 | **damage lands** — `ApplyActionResultToTarget` | `ApplyActionResultToTargets` (plural) |
| 12 | **chain** the next action's director | same |
| 22 | release the mutex, die | die |

Two details worth spelling out:

**Multi-hit is pipelined, not sequential.** At frame 12 the director spawns the *next* action's
director (picking single/multi by that action's own target count), while itself running to frame
22 — so consecutive hits overlap by 10 frames. Cure solves multi-hit with a strictly sequential
phase loop; Fire overlaps and uses the **`MAG002_FIRE_slotFree[7]` mutex** (one flag per entity
slot) to stop two overlapping hits on the *same* target from stacking: the next director stalls at
frame 0 until the previous one releases the slot at frame 22. The multi-target path doesn't use
the mutex at all.

**The flame cluster scales with the target.** Spawn positions are the target's effect anchor plus
a random offset in a cube of side `(2800 × entity.animation_speed_factor) >> 12`, capped at 1000 —
`animation_speed_factor` doubling as a model-size proxy (Cure derives size from the bbox; Fire uses
this cheaper field). Each flame also gets `ground_y` and is pushed 500–800 units away from the
floor if it spawned within 550 of it, plus a random scale `3328..4863` (Q12 ≈ 0.81–1.19).

## 3. The flame — `MAG_002_FIRE_Flame_Tick`

Node `TaskNodeFireFlame`. Waits `start_delay` frames (`rand%6 + 2×i` — staggered ignition), then
lives **16 frames**, drawing **two sprites** each frame:

1. **The flame** — `MAG002_FIRE_flameSprite`, `frame_index = frame` (a straight 16-keyframe
   animation), billboarded via `TransformCameraByShadowRotation(pos, scale, −(scale>>4))` — the
   lean angle derived from the random scale, so no two flames tilt alike.
2. **The ground light pool** — `MAG002_FIRE_groundGlowSprite` rotated 90° flat
   (`BuildRotationMatrixFromAngles((1024,0,0))`), scaled `(scale, 1.0, scale)`, with caller RGB
   `160 × clamp(pos_y)/2000 − 96` — a light pool on the floor whose **brightness tracks the
   flame's height**.

At frame 0 it populates the same pool with the secondary particles:

| Particle | Count | Motion (per frame) | Life |
|---|---|---|---|
| `MAG_002_FIRE_Ember_Tick` | 4 | `pos_y += vel_y; vel_y += vel_y>>5` (exponential rise), `scale −= scale>>6` | 16 frames |
| `MAG_002_FIRE_Spark_Tick` | 10 | `vel_x/z −= vel>>4` (decelerate), `vel_y += vel_y>>4` (rise), `scale −= 64` | `rand%4+5` frames |

## 4. The spark is a shared sprite, recoloured

The spark does **not** use a Fire-owned sequence. It calls
`EffectSprite_GetSharedSequence(5)` — an index into the shared `EFFECT_SELECTION_LIST` table —
and sets `ws.flags = 0x10` with `ws.clut_param[0] = 4`: **CLUT row +4**. That is the palette-
selection mechanism of the [sprite prim format](../cure-case-study/#the-sprite-sequences) doing
real work: one white spark artwork, recoloured per element by choosing a palette row. Expect other
elements' sparks to be the same sequence with a different `clut_param`.

It also plays a **random tail** of the animation: `frame_index = 9 − frames_left` with
`frames_left` starting at `rand%4+5`, so each spark begins at keyframe 1–4 and runs forward to
keyframe 9 — varied spark lengths for free.

## 5. 60 fps analysis — quarter-scaling

Like Cure, Fire is procedural with small integer dynamics, and every constant quarter-scales
cleanly for a smooth-60fps port (see the [Cure analysis](../cure-case-study/) for the approach):

| Element | 15 fps | 60 fps recipe |
|---|---|---|
| Timeline thresholds 1/6/8/12/22 | frames | 4/24/32/48/88 — compare-immediates |
| Flame life 16, sprite frames 0–15 | 1 keyframe/frame | 64 ticks; keyframe = `frame>>2` (hold) or lerp |
| Ember rise | `vel += vel>>5` | `vel += vel>>7` ((1+2⁻⁵)^¼ ≈ 1+2⁻⁷) |
| Ember shrink | `scale −= scale>>6` | `scale −= scale>>8` |
| Spark decel/accel | `vel ∓= vel>>4` | `vel ∓= vel>>6` |
| Spark shrink | `scale −= 64` | `scale −= 16` |
| Start delays | `rand%6 + 2i` | ×4 |
| Glow brightness | recomputed from `pos_y` | free — follows the smooth position |

Positions advance by `vel` per frame → per-tick `vel/4` needs a sub-unit accumulator for small
velocities (the nodes have spare fields). Damage at frame 8 → tick 32; the mutex and chaining are
frame-count comparisons and scale with the rest.

## 6. Node field maps

All four roles share the 36-byte pool; the payloads differ (`TaskNodeFireDirector` /
`TaskNodeFireFlame` / `TaskNodeFireEmber` / `TaskNodeFireSpark` in the IDB):

| Offset | Director | Flame | Ember | Spark |
|---|---|---|---|---|
| +12 | frame | frame | frame | **frames_left** (counts down) |
| +14 | action_index | start_delay | start_delay | start_delay |
| +16/+18/+20 | — | pos x/y/z | pos x/y/z | pos x/y/z |
| +22 | — | ground_y | **vel_y** | — |
| +24/+26/+28 | — | — | — | vel x/y/z |
| +28 | — | scale | scale | — |
| +32 | target_slot | — | — | scale |
| +34 | chain_timer | — | — | — |

## 7. Function reference

| Address | Name | Role |
|---|---|---|
| 0x629880 | `MAG_002_FIRE_FL` | loader (`mag001.tim` — dedicated, safe to edit) |
| 0x6298A0 | `MAG_002_FIRE_Init` | pools, mutex reset, camera, first director |
| 0x62A610 | `MAG_002_FIRE_RootTask` | VRAM double-buffer flip + queue driver |
| 0x62A380 | `MAG_002_FIRE_Director_SingleTarget` | 22-frame timeline, slot mutex, chaining |
| 0x629990 | `MAG_002_FIRE_Director_MultiTarget` | same timeline, one flame per target, plural applier |
| 0x629C10 | `MAG_002_FIRE_Flame_Tick` | flame + ground glow, spawns embers/sparks |
| 0x62A0A0 | `MAG_002_FIRE_Ember_Tick` | exponential rise, shrink |
| 0x629F90 | `MAG_002_FIRE_Spark_Tick` | shared sprite + CLUT recolour, random tail |
| 0x5710B0 | `EffectSprite_GetSharedSequence` | shared `EFFECT_SELECTION_LIST[id]` getter (engine-wide) |

Data: `MAG002_FIRE_flameSprite` (0xDEDC2C), `MAG002_FIRE_groundGlowSprite` (0xDEDDD8),
`MAG002_FIRE_emberSprite` (0xDEDF84) — all `EffectSpriteSequence`; `MAG002_FIRE_slotFree`
(0xDEE360, 7 dwords, 1 = free); `MAG002_FIRE_soundId` (0xDEE130); `MAG002_FIRE_cameraAnim`
(0xDED5FC); cast context / packet cursor / VRAM buffers at 0x24CBD60–0x24DFD6C.

## 8. Open questions

- **`animation_speed_factor` as a size proxy** — the field's name (community) says speed; Fire
  uses it to scale the spawn cube. Which is the true semantic (or both) is unverified.
- **`EFFECT_SELECTION_LIST`** — the shared sequence table: how many entries, which artwork is
  id 5, and which other effects use it (a `clut_param` survey across elements would confirm the
  recolour theory).
- ~~**Sign conventions**~~ **Resolved** ([Blizzard study](../blizzard-case-study/)): battle world
  **+Y is down** — the embers' negative `vel_y` is indeed upward.
- The unknown node fields (`unknown_16/18/1A/1E/20/22`) are zero-initialised and unread in the
  studied paths.
