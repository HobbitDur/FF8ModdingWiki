---
layout: default
parent: Battle
title: Battle Model Animation Timing (SLOW/FAST)
permalink: /technical-reference/battle/battle-model-animation-timing/
---

This page documents how battle model animations (characters, weapons, monsters) are
advanced per tick, and the engine's built-in half-step mechanism (`BATTLE_ANIM_FLAG_SLOW`)
that implements the Slow status — which turns out to be a complete, self-consistent
sub-frame interpolator that high-frame-rate mods can repurpose for smooth model motion.

1. TOC
{:toc}

## Delta-stream animation

Battle animations (monster/character .dat section 3) are bit-packed streams of per-frame
**deltas**. `Battle_ReadAnimation` consumes one frame per call:

- frame 0 is the absolute base pose (bones were zeroed at animation start), read in full;
- frames 1..N−1 are accumulative deltas: `root_pos += Δpos`, `bone.rot += Δrot` per bone;
- `current_frame` increments per call; `ProcessFieldEntitiesTransformation` then rebuilds
  the double-buffered render geometry;
- the bitstream offset and bit-reader state are saved back into `BattleAnimCmd` so the
  next call resumes where this one stopped.

Because the pose is a running sum of deltas, there is no closed form to re-sample — the
pose at frame N exists only by having applied frames 0..N. This is why a high-fps mod
cannot simply "evaluate the animation at t+0.5".

## BattleAnimCmd

| Offset | Field | Meaning |
|---|---|---|
| +0 | `current_animation_id` | Section 3 animation index |
| +1 | `flags` | See below |
| +2 | `current_byte_offset_in_bitstream` | Stream resume position |
| +4 | `interpolation_data` | Bit-reader sub-byte state |
| +6 | `current_frame` | Call counter (see SLOW semantics!) |
| +7 | `total_frames` | Completion threshold |

`flags` (`BattleAnimFlag`): bit 0 `SLOW`, bit 1 `FAST`, bits 2–3 = SLOW sub-frame
counter (a 1-bit toggle in practice), preserved bits used as `CONTINUOUS`/`UNK8` are
cleared at animation start.

## FAST (Haste status)

`FAST` sets the per-call loop count to 2 (`((flags>>1)&1)+1`): two frames' deltas are
read and applied per call. Animation plays at 2× speed and completes in half the calls.

## SLOW (Slow status) — a built-in half-step interpolator

With `SLOW` set, `Battle_ReadAnimation` behaves as follows (verified in disassembly):

- frame 0 (`current_frame == 0`) is still read in full — it is the absolute pose;
- for every later frame, all deltas are applied **halved** (`(x - sign) >> 1`, truncation
  toward zero);
- the bitstream offset is **only saved back when the sub-frame counter (flags bits 2–3)
  is 0**; the counter toggles 0↔1 every call. Net effect: each delta frame is read twice,
  as two halves, across two consecutive calls;
- `current_frame` increments every call — and the accounting is exact because
  `pre_Battle_ReadAnimation` sets **`total_frames = 2*nbFrames − 1`** when SLOW is set
  at animation start: 1 full call for frame 0 + 2 calls for each of the nbFrames−1 delta
  frames = 2·nbFrames−1 calls, so completion lands exactly when the stream is consumed.

So SLOW is not a hack — it is a complete half-rate player: duration doubles, motion is
halved per call with a genuine midpoint pose in between, completion stays exact. The only
imperfection is delta truncation (±1 unit per halved delta, wiped at each animation start
by the frame-0 absolute read).

## Where the flags are set

`Battle_QueueAnimation` clears SLOW|FAST and re-applies them from the entity's
`anim_status` (Slow/Haste status bits) on **every animation start** — and only when
`currentAnimSeqId == basedAnimSeq`, i.e. the idle/base loop. Attack choreography never
runs with SLOW/FAST in vanilla. The weapon `BattleAnimCmd` receives a copy of bits 0–1,
then `pre_Battle_ReadAnimation` (re)initializes both weapon and entity anim state.

Call graph (entity skeletal animations only):

```
AnimSeq VM (opcode < 0x80, opcode A0, idle restart)
    └─ Battle_QueueAnimation          ← the ONLY entity animation starter
         └─ pre_Battle_ReadAnimation  (reset state; total_frames ×2−1 if SLOW)
              └─ Battle_ReadAnimation
AnimSeq_UpdateEntityPerFrame (per tick)
    └─ AdvanceAnimationBy1AndCheckCompletion
         └─ Battle_ReadAnimation      (weapon then entity)
```

`pre_Battle_ReadAnimation` / `Battle_ReadAnimation` are **also** called directly by
magic/GF effect model animators (dozens of `MAG_*` functions) and by battle stage model
code (`BS_ReadGeometry`, `BS_RenderRelated`, `BS_ChangeStage`) — those anim_cmds never
pass through `Battle_QueueAnimation`, which matters when hooking.

## Choreography interactions (audited)

A full audit of `AnimSeq_DispatchActionOpcode` shows **no opcode reads or writes
`current_frame`** — sequences wait on animation *completion* (return value) or on
tick-based delays (`B9`, `delayBeforeNextAnimation`). Two opcodes touch animation
advancement at all:

- `BA` — manual single `AdvanceAnimationBy1AndCheckCompletion` call (rare; under SLOW it
  advances a half-step instead of a full frame);
- `AB` (Renzokuken) — sums `getAnimationFrameCount()` (read from the .dat data, not from
  `total_frames`) into the R1-trigger stage buckets; wall-clock timing is preserved under
  SLOW since each data frame still spans the same real time.

## Application: smooth models in high-frame-rate battle mods

At a 30fps battle loop (2 host frames per native 15fps tick), forcing SLOW on every
entity animation start gives native speed, native duration and **genuinely smooth
30 poses/s motion** — the engine does all the bookkeeping:

| Entity state | Vanilla flags | 30fps policy | Result |
|---|---|---|---|
| normal | none | force `SLOW` | 15 frames/s, poses update 30/s — smooth |
| Haste | `FAST` | clear `FAST` (plain) | 30 frames/s, one frame per call — smooth |
| Slow | `SLOW` | keep `SLOW` + hold 1-in-2 | 7.5 frames/s (vanilla appearance) |

Hooking notes (FF8 2000 US/EN 1.2):

- Set the policy inside `Battle_QueueAnimation` — after its status logic, before its
  `pre_Battle_ReadAnimation` calls (which read the flag to double `total_frames`). A
  wrapper flag ("inside queue-animation") lets a `pre_Battle_ReadAnimation` hook apply
  the policy to exactly the entity+weapon anim_cmds and nothing else.
- Effect and stage model animations do not pass through `Battle_QueueAnimation`; they
  need their existing pacing (effect frame-hold / hold-gate) left in place. Never hold a
  `Battle_ReadAnimation` call made from inside a held effect tick — the effect gate
  already paces the whole tree.
- At 60fps (4 host frames per tick) the engine only offers ÷2, so with **vanilla data**:
  normal = SLOW + a 1-in-2 hold (30 poses/s — twice as smooth as a plain hold),
  Haste = SLOW alone (fully smooth), Slow = SLOW + 3-of-4 hold. Feeding the engine data
  already converted to 30 fps lifts that ceiling to a genuine 60 poses/s — see
  [60 poses/s: 30 fps data × the engine's half-step](#60-poses-per-second) below.
- **Completion early-out gotcha**: when `current_frame >= total_frames`,
  `Battle_ReadAnimation` returns COMPLETE immediately **without calling
  `ProcessFieldEntitiesTransformation`** — no geometry rebuild. Vanilla never exposes
  this (the choreography VM runs every tick and requeues the looping animation in the
  same call), but any mod that gates the VM to a subset of host frames will see a
  1-frame flicker whenever a completion surfaces on a non-VM frame, since the entity's
  double-buffered geometry goes stale for that frame. SLOW makes it systematic: loops
  last 2T−1 calls (odd), so the completion parity keeps landing on held frames. Fix: a
  `Battle_ReadAnimation` hook must rebuild the geometry itself before returning COMPLETE
  for already-finished animations.

## 60 poses/s: 30 fps data × the engine's half-step
{: #60-poses-per-second }

The engine only offers ÷2, and inserting frames only offers ×N. **Doing both multiplies**:
convert the data to 30 fps (`factor = 2`, see
[Animation frame-rate conversion](../animation-frame-rate-conversion/)) and force SLOW at a
60 fps host tick. The engine then reads each of the doubled frames twice, as two halves:
4 poses per original 15 fps frame, at native wall-clock speed.

For an animation of `n` original frames, `m` frames once converted to 30 fps
(`m = 2n` looping, `2n-1` played once):

| Entity state | Flags | Data frames per second | Result |
|---|---|---|---|
| normal | force `SLOW` | 30 | native speed, **60 poses/s** |
| Haste | clear `SLOW` | 60 | 2× speed (`n/30` s), 60 poses/s |
| Slow | force `SLOW` + hold 1-in-2 | 15 | ½ speed (`2n/15` s), 30 poses/s |

Every state is smooth, and each keeps its vanilla duration. The reason it works is that
**Slow status stops being expressed through the frame count**: SLOW is always on as the
interpolator, and the real Slow status becomes a host-side hold. `total_frames` is then
`2m-1` whatever the status, instead of doubling when a monster happens to be slowed — the
128 frame Slow limit disappears as a special case.

### What it costs

The call counter is the wall: `current_frame` and `total_frames` are bytes, so the whole
animation must play in ≤ 255 calls. Under SLOW that means `2m-1 = 4n-3 ≤ 255`, i.e.
**n ≤ 64 original frames** — the same boundary as 60 fps data (`(n-1)*4+1 ≤ 255`), reached
with **half the frame data**.

Over the 199 readable `c0m` files (4779 animations):

| Approach | Animations needing a split | Data size |
|---|---|---|
| 60 fps data (`factor = 4`) | 117 (the 255 limit, plus the 128 Slow limit on idles) | ×4 |
| 30 fps data + forced SLOW | **36** (the byte call counter only) | ×2 |

The 36 are exactly the animations longer than 64 frames; they are split like any other
(and the `A0` ones stay manual). Everything else — including every idle looped by `A0`,
the case that blocks 60 fps data — needs no data change at all.

Vanilla data with forced SLOW at a 30 fps host tick remains the near-zero-cost option for
30 poses/s: no file is touched. Forcing SLOW does extend the byte call counter to every
animation though, so the two vanilla animations over 128 frames overflow it and have to be
split (or left unforced): **Elvoret `c0m091` and Elnoyle `c0m131`, animation 27, 140 frames**
— `2*140-1 = 279 & 0xFF = 23`, i.e. the animation would stop after 23 calls. Every other
vanilla animation is 128 frames or shorter.

## Function and data addresses

| Name | Address | Description |
|---|---|---|
| `Battle_ReadAnimation` | `0x508F90` | Per-call delta reader (SLOW/FAST logic inside) |
| `pre_Battle_ReadAnimation` | `0x509440` | Animation start: resets state, `total_frames = 2n−1` if SLOW |
| `Battle_QueueAnimation` | `0x509520` | Entity animation starter; applies Slow/Haste status to flags |
| `AdvanceAnimationBy1AndCheckCompletion` | `0x5094F0` | Per-tick advance (weapon + entity) |
| `AnimSeq_UpdateEntityPerFrame` | `0x504290` | Choreography VM driver |
| `AnimSeq_DispatchActionOpcode` | `0x504BB0` | Sequence opcode dispatcher (audited: no `current_frame` access) |
| `ProcessFieldEntitiesTransformation` | `0x508C90` | Rebuilds render transform/geometry |
| `getAnimationFrameCount` | — (see IDA) | Reads nbFrames from animation data (used by opcode `AB`) |
