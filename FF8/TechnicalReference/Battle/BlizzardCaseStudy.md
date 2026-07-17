---
layout: default
parent: Battle
title: "Case study: Blizzard animation"
permalink: /technical-reference/battle/blizzard-case-study/
---

The fourth worked spell animation — **Blizzard** (effect_id 144, `mag143.tim`) — after
[Firaga](../firaga-case-study/), [Cure](../cure-case-study/) and [Fire](../fire-case-study/).
Blizzard is a timeline effect like Fire, but it contributes the two biggest new mechanisms so far:

- **a real 3D mesh** — the ice crystal is triangle geometry in `.data`, not a billboard;
- **per-triangle mesh shattering** — at impact, each triangle of the crystal becomes an
  independent shard with its own delay, spin and outward flight, precomputed from the mesh itself.

It also settled a long-open question: **battle world +Y is down** (see §5).

Addresses are `FF8_EN.exe`; everything below is named and commented in the IDB.

1. TOC
{:toc}

## 1. Structure

Same skeleton as Fire: a header-only root task (here the *shared* `au_re_BdlinkTask_30`, not an
effect-private copy) plus **one** 0x24 × 150 particle pool holding everything — director, crystal,
mist, falling ice, debris, shockwave. One director per action, target slot in the node,
`MAG144_BLIZZARD_cameraAnim` + TIM upload on cast.

## 2. The director — a 44-frame timeline

`MAG_144_BLIZZARD_Director` (0x61AC70), damage at the **impact**:

| Frame | Event |
|---|---|
| 0 | resolve the head anchor (bone 0xF0, +0x1000); **build the shard table** (§4) |
| 1 | spawn the **crystal** 900 above the target; SFX 3D |
| 2–27 (odd) | 1 **mist puff** per odd frame, ~1000 above, static, fading |
| 18–32 | 2–3 **falling ice** sprites per frame, gravity-accelerated |
| 28 | **chain** the next action's director (pipelined multi-hit, like Fire but 28 frames apart; no slot mutex) |
| 37 | **impact**: `ApplyActionResultToTarget`, ground **shockwave**, camera shake |
| 37–39 | 20 **debris** per frame (60 total) scattering horizontally |
| 44 | die |

## 3. The crystal — a 3D mesh with a choreographed slam

`MAG_144_BLIZZARD_Crystal_Tick` (0x61B740) draws `MAG144_BLIZZARD_crystalMesh` +
`MAG144_BLIZZARD_crystalPrims` through the 208-byte geometry workspace — the same class of
renderer as Cure's overlay, not a sprite. Its motion:

- frames 0–27: spins (`angle += vel; vel −= vel/10` — fast spin settling);
- frames 28–32: a small **lift** (`y −= 80`, decaying — remember −Y is up);
- frames 35–36: the **slam** — two steps of `(crystal_y − ground_y + 196)/2`, which lands the
  crystal at exactly `ground_y − 196` **regardless of its height**. No tuning constant: the landing
  is computed;
- frame 37: `BATTLE_CAMERA_SHAKE_OFFSET += 32` — the impact shake, same frame the director applies
  damage;
- frames 40–47: fade-out via a blend-mode switch (`rgb=0`, mode `0xC3`), then dies at 48.

The impact **shockwave** (`MAG_144_BLIZZARD_Shockwave_Tick`) is also 3D — a prim model drawn via
the shared `Effect_RenderPrimModel`, scaled `(1, s, s)` with a decaying growth rate: a ring
expanding on the ground, fading with the same `0xC3` switch.

## 4. The shatter — per-triangle shards

The headline mechanism. `MAG_144_BLIZZARD_ShatterPrep_BuildShards` (0x61B190) walks the crystal
mesh's triangle list at cast time and emits one 32-byte **`BlizzardShard`** per triangle (up to 80,
in a per-action 2560-byte buffer):

| Field | Value |
|---|---|
| centroid | `(v0+v1+v2)/3` |
| start_delay | `rand%3 − (8·centroid_y + 18304)/3958 + 8` — **height-dependent: the crystal shatters bottom-up** (−Y up) |
| spin | two random angular velocities `±32·(r&7)`, `±16·(r>>3&7)` |
| flight | direction = `normalize(centroid_x, 0, centroid_z)` — horizontally **outward from the crystal's axis** — distance `3500..8499` over `12..19` frames |

The crystal renderer draws each triangle as part of the intact mesh until its shard's delay
expires, then flies and spins it independently. The shatter is therefore **derived from the
geometry** — re-model the crystal and the debris pattern adapts by construction. Nothing else in
the four case studies generates its animation *from* its mesh like this.

## 5. The Y-axis, settled

Blizzard provided the decisive evidence for a question Cure and Fire left open: **battle world
+Y is down.** The falling ice accelerates with *positive* `vel_y` (`vel += vel>>6` — gravity);
the crystal spawns at `y − 900` (visibly above) and slams *down* by subtracting toward
`ground_y`; Fire's rising embers use negative velocities; and the shard delay decreases with
`+centroid_y` — bottom-up. Consequences propagated to the other studies: Cure's helix starts at
the **feet** and sweeps up; its sparkles drift gently downward.

## 6. 60 fps analysis

Same quarter-scaling story as Fire and Cure, with one new wrinkle: the crystal's motion is
per-frame arithmetic (`vel −= vel/10` → `vel −= vel/40`-ish per tick; the slam's two computed
steps become eight), and the **shard table needs its durations and delays ×4 with `spin_vel`,
`fly_speed_q` and `lifetime_q` ÷4** — all integer fields in a table we now have a struct for, so a
60 fps port could simply post-process the table after `ShatterPrep` builds it. The height-ordered
shatter and computed slam landing survive scaling untouched since both are derived, not tuned.

## 7. Function reference

| Address | Name | Role |
|---|---|---|
| 0x61AB80 | `MAG_144_BLIZZARD_FL` | loader (`mag143.tim`) |
| 0x61ABA0 | `MAG_144_BLIZZARD` | init: pools, camera, first director |
| 0x61AC70 | `MAG_144_BLIZZARD_Director` | 44-frame timeline, chaining at 28, damage at 37 |
| 0x61B160 / 0x61B190 | `MAG_144_BLIZZARD_ShatterPrep(_BuildShards)` | mesh → per-triangle `BlizzardShard` table |
| 0x61B740 | `MAG_144_BLIZZARD_Crystal_Tick` | 3D crystal: spin, lift, computed slam, shake, fade |
| 0x61B900 / 0x61B9A0 | `MAG_144_BLIZZARD_CrystalRender(_Core)` | mesh + flying-shards renderer |
| 0x61B660 | `MAG_144_BLIZZARD_MistPuff_Tick` | static fading puff (8 frames) |
| 0x61B5B0 | `MAG_144_BLIZZARD_FallingIce_Tick` | gravity sprite (`vel += vel>>6`) |
| 0x61B4F0 | `MAG_144_BLIZZARD_Debris_Tick` | horizontal scatter (`vel −= vel>>4`) |
| 0x61B3A0 | `MAG_144_BLIZZARD_Shockwave_Tick` | 3D expanding ground ring (`Effect_RenderPrimModel`) |

Data: `MAG144_BLIZZARD_crystalMesh` (0xDD8590), `crystalPrims` (0xDD9280), `shardBuffers`
(0x24BB968, 2560 B/action), `mistSprite` (0xDD82F0), `iceSprite` (0xDD83E4, shared by falling ice
and debris), `shockwaveModel` (0xDD8D48), `soundId` (0xDD9A38), `cameraAnim` (0xDD7918).

## 8. Open questions

- **The crystal mesh format** (`crystalMesh`/`crystalPrims`) is decoded only as far as the shard
  prep reads it (triangle count + 10-word records with vertex indices at words 2–4, vertices at
  +8). `CrystalRender_Core` (0x61B9A0, the largest function) was classified by its callers and
  usage, not read line-by-line — the full mesh/prim format and the intact-vs-shard draw switch
  live there.
- The mist/ice **sprite sequences** were not byte-checked against the `24 05 01 00` signature
  (they were typed by usage).
- Whether **Blizzara/Blizzaga** (effect 103/104) reuse the crystal mesh or the shard mechanism —
  the natural follow-up.
