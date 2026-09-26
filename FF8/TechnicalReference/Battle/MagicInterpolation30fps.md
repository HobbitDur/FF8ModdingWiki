---
title: Magic effect interpolation (30 fps)
layout: default
parent: Battle
permalink: /technical-reference/battle/magic-interpolation-30fps/
nav_order: 5
author: HobbitDur
---

# Magic effect interpolation to 30 fps

Battle logic runs at 15 fps. Rendering every spell at a real 30 fps means inserting **one interpolated
in-between frame per native frame** (phase = ½): on that extra frame each live effect part is re-drawn at
its half-way pose, while the game's logic does not advance. Battle timing, damage frames and action
sequencing are unaffected — only visual frames are added.

This page describes how **magic effects** are interpolated. It builds on
[Magic effect anatomy](MagicEffectAnatomy.md), which documents the draw engines and each spell's data.
The sibling problem for character and monster models is covered in
[Animation frame-rate conversion](AnimationFrameRateConversion.md). The overview of every effect family and
of the FFNx True30FPS implementation (native effect code, verification, in-between frames) is
[Battle effects and true 30 fps](BattleEffects30fps.md).

## The mechanism

Each spell's task routines have a native copy in FFNx, verified tick by tick against the original (see
[Battle effects and true 30 fps](BattleEffects30fps.md)). On a real tick the copy runs exactly like the
original and additionally remembers what it drew: each part's position, size, spin, colour and the
packet it built. On the in-between frame the copy **only draws**: every part is drawn from that memory,
moved half way to the state its own update computes for the next tick. The in-between frame never
advances the effect, never draws a random number and never plays a sound, so battle timing, damage
frames and action sequencing are unaffected.

## The two interpolation methods

Every animated quantity in the magic system reduces to one of two exact operations.

**Method A — velocity nudge.** For integrated fields (position, spin, scale, size, colour that advance by
`x += v`), the mid-frame value is `x + v/2`. This is exact rather than approximate: every particle tick
runs in the order *read → draw → advance → mutate velocity*, so the velocity is constant for the whole
duration of a tick and motion between two consecutive native states is perfectly linear.

**Method B — fractional-frame recompute.** For motion expressed in closed form against the frame counter
(morph alpha, pose-blend factors, colour and flash ramps, `sin(frame)` scales), the mid-frame value is
`f(frame + 0.5)`.

A part uses A, B, or both.

## Handling per draw engine

The magic system draws through a small fixed set of engines, so the plan is expressed per engine rather
than per spell. Between them these cover all 49 castable spells.

| Draw engine              | Interpolation                                                                                                                                                                                                                                                                                                                                                                                 |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Prim model               | Nudge the render header's animated fields — `color_param`, spin, scale (Method A). Scales driven by `sin(frame)` use Method B.                                                                                                                                                                                                                                                                |
| Sprite sequence          | The particle's **position** interpolates (Method A). The `frame_index` flipbook does not — discrete artwork has no half-frame, so it holds at 15 fps, or optionally cross-fades two adjacent art frames.                                                                                                                                                                                      |
| Generic heal-sprite      | The emitter is a bone-follow anchor and interpolates for free once the target model does; leaf particles use Method A.                                                                                                                                                                                                                                                                        |
| Data-driven heal emitter | Each particle in the 89-slot pool is nudged (Method A) before the held redraw.                                                                                                                                                                                                                                                                                                                |
| Status keyframe-model    | The pose-blend factor in the element descriptor is Method B; the descriptor's position and scale are Method A.                                                                                                                                                                                                                                                                                |
| GTE vertex-morph         | The morph alpha is `sin(frame)`, so the vertex lerp is recomputed at `frame + 0.5` (Method B).                                                                                                                                                                                                                                                                                                |
| Cinematic bone-stream    | The next tick is computed ahead on saved state (the script steps and the per-bone speed/acceleration integration run, with sounds, loads and damage skipped), then everything is put back. Bone outputs, node matrices and light sets are drawn half way between the two ticks; a bone that jumps, respawns or changes its draw routine holds. Randomised channels keep their 15 fps samples. |
| Animated model container | Standard skeletal interpolation: bone matrices lerp between animation keyframes.                                                                                                                                                                                                                                                                                                              |
| Procedural geometry      | Vertex buffers are rebuilt each frame from parameters, so they are recomputed at `frame + 0.5` (Method B), or consecutive buffers are lerped.                                                                                                                                                                                                                                                 |
| Fullscreen 2D overlay    | Script-gated frames; the quad transform interpolates if animated, otherwise it holds.                                                                                                                                                                                                                                                                                                         |

## Spells covered

The Fire (Fire, Fira, Firaga), Thunder (Thunder, Thundara, Thundaga) and Ice (Blizzard, Blizzara, Blizzaga)
families have native copies with in-between frames; the other spells follow family by family. A spell
without a native copy uses the generic in-between frame: the packets of the last tick are redrawn with a
position correction. The per-family status is kept on
[Battle effects and true 30 fps](BattleEffects30fps.md#status-ffnx-true30fps).

Per family, the in-between frame of the covered spells is:

| Spell    | Parts moved half way                                                                             | Parts that hold                  |
|----------|--------------------------------------------------------------------------------------------------|----------------------------------|
| Fire     | sparks (position, size), embers (height, size)                                                   | flame flipbook                   |
| Fira     | flame column and burst (spin, width, height), trail and sparks, shock ring colour                | trail table value                |
| Firaga   | flame swirl (spin, size), burst and fireball size, orbiting sparks (angle)                       | area flames                      |
| Thunder  | —                                                                                                | bolt layers, ground layer, flash |
| Thundara | glows, column and flash ball at the exact fractional frame, sparks, fading layer colour          | sprite layers, flashes           |
| Thundaga | lightning model (prim-model player in between), debris (position, size, spin), shards, sparks    | UV scroll step, flashes          |
| Blizzard | crystal (spin, height, glint scroll, flying shards), shockwave, debris, falling ice, mist colour | flipbook frames                  |
| Blizzara | growing block (height, UV scroll), shards (centre, angles, colour), pillar, burst, chunks, mist  | newly broken shards              |
| Blizzaga | frozen target band, block growth morph, ring, flash model, sparkles, mist, flakes                | ribbon and spiral trails         |

## Cases to leave alone

Some things resist interpolation by nature and are better accepted than fought.

- **Flipbook sprite artwork** (the fire flame, bolt flicker) holds at 15 fps. On fast, brief particles this
  is imperceptible, and on the dominant flipbooks it often reads as intentional.
- **Random-jitter channels** (cinematic randomised bone channels, splash noise) are stochastic; there is no
  curve between samples, so they hold.
- **Discrete spawn events.** A particle's appearance is instantaneous. Its motion is interpolated *after* it
  exists; nothing is ever spawned on an in-between frame.

## Addresses

| Symbol                                               | Address  |
|------------------------------------------------------|----------|
| `Effect_RenderPrimModel`                             | 0x572200 |
| `InitEffectSequenceFromData`                         | 0x571C80 |
| `MAG_025_CURA_DrawSprite` (generic heal-sprite draw) | 0x88A0F0 |
| `Effect_ParticleEmitter_AllocParticle`               | 0x881700 |
| `Effect_Particle_DrawAndAdvance`                     | 0x880510 |
| `MAG_119_STOP_RenderKeyframedModelElement`           | 0x6BF410 |
| `MAG_222_WATER_CinematicRootTick`                    | 0xA9B870 |
| `MAG_222_WATER_CinematicBoneStreamDecoder`           | 0xAA1810 |
| Cinematic bone VM stepper                            | 0xAA4F60 |
| `GfCinematic_CommitBoneAngles`                       | 0xAA17D0 |
| `Effect_BindModelContainerSetAnim` (reaper)          | —        |
| `Effect_SetScreenFlash`                              | 0x5713E0 |
