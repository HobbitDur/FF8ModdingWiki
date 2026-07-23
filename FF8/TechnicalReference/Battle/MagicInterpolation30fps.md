---
title: Magic effect interpolation (30 fps)
layout: default
parent: Battle
permalink: /technical-reference/battle/magic-interpolation-30fps/
nav_order: 5
---

# Magic effect interpolation to 30 fps

Battle logic runs at 15 fps. Rendering every spell at a real 30 fps means inserting **one interpolated
in-between frame per native frame** (phase = ½): on that extra frame each live effect part is re-drawn at
its half-way pose, while the game's logic does not advance. Battle timing, damage frames and action
sequencing are unaffected — only visual frames are added.

This page is the implementation plan for **magic effects**. It builds on
[Magic effect anatomy](MagicEffectAnatomy.md), which documents the draw engines and each spell's data.
The sibling problem for character and monster models is covered in
[Animation frame-rate conversion](AnimationFrameRateConversion.md).

## The mechanism

Interpolation reuses the **hold**: the effect's memory window is snapshotted, its tick is run (the tick
draws), and the window is restored. The effect therefore draws an extra time without advancing. For 30 fps
the effect is held **once**; the interpolation nudge is applied immediately before the held redraw, so the
extra frame lands halfway between two native poses.

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

| Draw engine | Interpolation |
|---|---|
| Prim model | Nudge the render header's animated fields — `color_param`, spin, scale (Method A). Scales driven by `sin(frame)` use Method B. |
| Sprite sequence | The particle's **position** interpolates (Method A). The `frame_index` flipbook does not — discrete artwork has no half-frame, so it holds at 15 fps, or optionally cross-fades two adjacent art frames. |
| Generic heal-sprite | The emitter is a bone-follow anchor and interpolates for free once the target model does; leaf particles use Method A. |
| Data-driven heal emitter | Each particle in the 89-slot pool is nudged (Method A) before the held redraw. |
| Status keyframe-model | The pose-blend factor in the element descriptor is Method B; the descriptor's position and scale are Method A. |
| GTE vertex-morph | The morph alpha is `sin(frame)`, so the vertex lerp is recomputed at `frame + 0.5` (Method B). |
| Cinematic bone-stream | Bone output angles are **matrix-lerped** between virtual-machine keyframe steps. The stepper walks the bone order list across three channels per bone; each channel holds a stream pointer and a wait counter decremented by a per-bone speed, and runs opcodes when the counter expires — that speed is the temporal lever. Deterministic channels interpolate; **random channels do not** and hold. |
| Animated model container | Standard skeletal interpolation: bone matrices lerp between animation keyframes. |
| Procedural geometry | Vertex buffers are rebuilt each frame from parameters, so they are recomputed at `frame + 0.5` (Method B), or consecutive buffers are lerped. |
| Fullscreen 2D overlay | Script-gated frames; the quad transform interpolates if animated, otherwise it holds. |

## Prerequisite: hold-safety

Interpolation via the snapshot hold only applies to effects that are safe to hold, which gates a large
part of the roster.

- Roughly **26 spells are holdable today** (the offensive-timeline and heal tiers) and can be interpolated
  immediately.
- The **17 never-held arena spells** (the ‑ara/‑aga tiers and the status thunks) build their state inside a
  fixed arena double-buffer that lies outside any snapshot window. They require **two-region holdability**
  first; this is a real engineering task, not a nudge.
- The **cinematic tier** is not snapshot-held at all. It is gated instead through its `paused` flag — the
  same approach used for GF summons — and interpolated by matrix-lerp.

## Roadmap

**Phase 0 — mechanism.** Adapt the existing hold to a single 30 fps mid-frame (phase ½).

**Phase 1 — the holdable spells.** Wire Method A/B nudges for the offensive-timeline and heal tiers. Each
spell's exact animated fields are already catalogued. This is the highest visual payoff for the least risk.

**Phase 2 — arena holdability.** Implement a two-region snapshot covering the arena double-buffer, which
unlocks the 17 never-held spells; the same nudges then apply.

**Phase 3 — matrix tiers.** Cinematic effects (bone-lerp via the channel wait speed), the reaper model
container, and GF summons.

**Phase 4 — procedural geometry.** Quake's ground mesh, Tornado's funnel and Holy's gather grid, recomputed
at `frame + 0.5`.

## Cases to leave alone

Some things resist interpolation by nature and are better accepted than fought.

- **Flipbook sprite artwork** (the fire flame, bolt flicker) holds at 15 fps. On fast, brief particles this
  is imperceptible, and on the dominant flipbooks it often reads as intentional.
- **Random-jitter channels** (cinematic randomised bone channels, splash noise) are stochastic; there is no
  curve between samples, so they hold.
- **Discrete spawn events.** A particle's appearance is instantaneous. Interpolate its motion *after* it
  exists — never spawn on a held frame, or particles double.

## Addresses

| Symbol | Address |
|---|---|
| `Effect_RenderPrimModel` | 0x572200 |
| `InitEffectSequenceFromData` | 0x571C80 |
| `MAG_025_CURA_DrawSprite` (generic heal-sprite draw) | 0x88A0F0 |
| `Effect_ParticleEmitter_AllocParticle` | 0x881700 |
| `Effect_Particle_DrawAndAdvance` | 0x880510 |
| `MAG_119_STOP_RenderKeyframedModelElement` | 0x6BF410 |
| `MAG_222_WATER_CinematicRootTick` | 0xA9B870 |
| `MAG_222_WATER_CinematicBoneStreamDecoder` | 0xAA1810 |
| Cinematic bone VM stepper | 0xAA4F60 |
| `GfCinematic_CommitBoneAngles` | 0xAA17D0 |
| `Effect_BindModelContainerSetAnim` (reaper) | — |
| `Effect_SetScreenFlash` | 0x5713E0 |
