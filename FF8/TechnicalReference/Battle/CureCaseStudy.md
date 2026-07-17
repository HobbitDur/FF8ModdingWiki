---
layout: default
parent: Battle
title: "Case study: Cure animation"
permalink: /technical-reference/battle/cure-case-study/
---

A second worked spell animation — **Cure** (effect_id 1) — to sit alongside the
[Firaga case study](../firaga-case-study/). Firaga and Cure are the **two archetypes** of the
in-engine spell effects:

- **Firaga = a director on a frame timeline.** One task counts frames 0→60 and spawns
  particles at hardcoded frame numbers.
- **Cure = a state machine.** One task dispatches the current **phase handler** from a jump
  table (indexed by a phase byte), and phases advance themselves. This same framework is shared
  by the whole **heal/status family** (Cure, Double, the shared `MagicEffect05`, …).

Knowing both patterns is enough to read essentially every regular spell — see the
[Fire case study](../fire-case-study/) for the timeline archetype in its simplest form (plus
patterns neither of the other two has: target-count dispatch, pipelined multi-hit with a slot
mutex, shared palette-recoloured sprites). Read
[Magic Effect Anatomy & Authoring](../magic-effect-anatomy/) for the shared model; addresses are
the **2013 Steam English `FF8_EN.exe`**. Fujin shows these functions live.

> Two things make Cure worth reading closely, and neither is visible from the director alone:
> its phase 3↔4 pair is a **loop over the cast's targets**, and its visual is a **helix whose
> every dimension is derived from the target's own model** — nothing about Cure's size is
> hardcoded.

1. TOC
{:toc}

## 1. Dispatch and the shared atlas

```
kernel "Cure" magic entry +0x04 = 1
   Magic_GetIDLoad(1) @0x50AF20   idx = 0
      MagicList_TextureLoad[0] = 0x8D69E0  MAG_001_CURE_FL   → loads mag000-049.tim
      MagicList_Logic[0]       = 0x8D6A00  MAG_001_CURE_Init
```

> **The real Cure init is `0x8D6A00`.** The community IDB also has a function labelled
> `MAG_001_CURE` at `0x88CF70`, but the dispatch table does **not** point there — `0x88CF70` is
> only referenced from `MagicList_Logic + 0x5C` (slot 23 = effect_id 24), i.e. it is actually
> **Esuna's** init, mislabelled. Always trust the table (`0xC81774 + 4·(id−1)`), not a name.

The loader:

```c
int MAG_001_CURE_FL() { dword_277AEC0 = IO_GetFile_MAGIC("mag000-049.tim"); }
```

**`mag000-049.tim` is a shared atlas** — one 512×256 texture used by the whole block of
effects 0–49 (the cures, status spells, etc.), *not* a Cure-only file like Firaga's `mag142.tim`.
This matters for modding (see [§8](#8-how-to-modify-cure)).

## 2. Init — `MAG_001_CURE_Init` @0x8D6A00

Unlike Firaga's two queues, the heal framework sets up **four** BdLink task pools — a root pool
plus three parallel sub-effect pools that the director ticks every frame:

| Pool | Node size × count | Role |
|---|---|---|
| `unk_277AFC0` (root) | 0x64 × 2 | holds the director task |
| `stru_278A228` | 0x58 × 4 | emitters (one per target; applies the heal) |
| `stru_277BF70` | 0x6C × 300 | the helix + its sparkles and motes (§6) |
| `stru_278C788` | 0x5C × 100 | glints (§6) |

It adds the director with `Effect_AddTaskAndInitFromCtx` (the shared "add task + copy target
info from the cast context" helper), plays a hardcoded camera (`MAG001_CURE_cameraAnim`), uploads
the texture, initialises three VRAM cursors, and returns the root queue.

## 3. The state-machine director — `MAG_001_CURE_Tick` @0x8D6B30

```c
int MAG_001_CURE_Tick(int task_node) {
  qmemcpy(&unk_2793E58, &BD_LINK_TASK_HEADER_CAMERA.data, 0x20u);  // snapshot camera
  v4[0]  = MAG_001_CURE_State00_Advance;
  v4[1]  = MAG_001_CURE_State01_Advance;
  v4[2]  = MAG_001_CURE_State02_WaitUnlocked;
  v4[3]  = MAG_001_CURE_State03_SpawnEmitter;
  v4[4]  = MAG_001_CURE_State04_NextTargetLoop;
  v4[5]  = MAG_001_CURE_State05_Advance;
  v4[6]  = MAG_001_CURE_State06_WaitSubQueuesEmpty;
  v4[7]  = MAG_001_CURE_State07;
  v4[8]  = MAG_001_CURE_State08;
  v4[9]  = MAG_001_CURE_State09_Finish;
  v4[10] = nullsub_959;
  Effect_UpdateTargetPosFromBones(task_node);          // recompute target position
  ( v4[ task_node->phase ] )(task_node);               // dispatch the current phase
  ExecuteTaskQueue(&stru_278A228);                     // run the 3 sub-effect queues
  ExecuteTaskQueue(&stru_277BF70);
  ExecuteTaskQueue(&stru_278C788);
  ++task_node->frame;
  if ( finished_flag && !locked ) { Effect_ReleaseLinkedTask(task_node); return 2; }
  return 0;
}
```

The key difference from Firaga: **the behaviour lives in the phase byte** (`task_node + 41`),
not in a frame counter. Each frame the director calls the current phase handler, which decides
when to move on. The phase handlers (all tiny):

| Phase | Handler | Does |
|---|---|---|
| 0 | `State00_Advance` | `++phase` (one-frame pacer) |
| 1 | `State01_Advance` | `++phase` |
| 2 | `State02_WaitUnlocked` | `++phase` only once a lock byte clears |
| 3 | `State03_SpawnEmitter` | spawns `MAG_001_CURE_Emitter_Tick` into the emitter pool, sets `emitter_spawned`, `++phase` |
| 4 | `State04_NextTargetLoop` | **loops back to phase 3 for the next target/hit** — see below |
| 5 | `State05_Advance` | `++phase` |
| 6 | `State06_WaitSubQueuesEmpty` | `++phase` **only once every sub-queue has drained** |
| 7–8 | `State07/08` | pacers |
| 9 | `State09_Finish` | sets the "finished" flag (`+38 |= 1`), `++phase` |
| 10 | `nullsub_959` | no-op (idle until the queues drain) |

So Cure's timeline is: pace in → **spawn a heal emitter per target** (phases 3↔4) → mark finished
(phase 9) → idle until the sub-queues empty → director releases its linked task and dies.

### Phase 4 is a target loop, not a timed hold

This is the load-bearing detail. `State04_NextTargetLoop` **decrements** the phase:

```c
if (!director->emitter_spawned_flag) {              // an emitter/ring is still playing -> wait
    if (director->action_index >= director->action_count_limit)
        ++director->state_phase;                    // all actions done -> phase 5
    else {
        ++director->action_index;
        ++director->loop_iteration_count;
        director->state_phase -= 1;                 // -> back to State03, spawn the next emitter
    }
}
```

Two facts confirm it is an **action/target** loop and not a duration:

- `Init` loads `action_count_limit` (+88) from `cast_context->action_data->actionCountMinus1` —
  an **action count**.
- `Emitter_State2_ApplyHeal` heals `action_data[action_index].targetData[subtarget_index]`,
  indexed by the **same counter** the loop increments.

The handshake is the `emitter_spawned` byte (+99): phase 3 sets it, and the **ring task clears it
on death** (`root_director->emitter_spawned_flag = 0`), which releases phase 4 to advance. That is
how one Cure director serves a multi-target Curaga: one emitter, one helix and one heal per target,
strictly sequenced.

Phase 6 is likewise not a pacer — it blocks on the sub-queue survivor count, so the director cannot
die while sparkles are still on screen.

## 4. The shared heal/status framework

Three helpers in `MAG_001_CURE_Tick` are **not** Cure-specific — Cure, Double and the shared
`MagicEffect05` all use them (named neutrally for that reason):

| Function | Address | Role |
|---|---|---|
| `Effect_AddTaskAndInitFromCtx` | 0x8DC540 | add a task to a pool + copy target/entity info from the cast context |
| `Effect_UpdateTargetPosFromBones` | 0x8DC740 | recompute the target's effect position each frame (bones 0xF0/0xF1) |
| `Effect_ReleaseLinkedTask` | 0x8DC530 | decrement the lock on a linked task on exit |

`MagicEffect05_Tick` (0x8D4530) is the clearest sibling: identical shape (phase jump table +
`Effect_UpdateTargetPosFromBones` + four sub-queues + `Effect_ReleaseLinkedTask`), just
different phase handlers. When you understand Cure you understand that whole family.

### Confirmed on a second spell: Esuna (24)

`MAG_024_ESUNA_Init` (0x88CF70) was read specifically to test whether the framework generalises
beyond Cure and its immediate siblings. It does, point for point:

- it builds its director pool and calls **`Effect_AddTaskAndInitFromCtx`** with the same
  `(pool, tick_fn, 100, 0)` shape;
- it allocates **four pools** — `0x64×2` director, `0x58×4`, `0x2A4×3`, `0x40×10`;
- it lays out **three packet arenas** at `base`, `base+0xA000`, `base+0x14000`, each with the
  paired cursor globals Cure uses;
- it reads the cast context identically (`action_data` at +4, counts at +16/+17).

Two details are worth keeping. First, **Esuna reuses Cure's camera track** —
`Battle_PlayCameraAnimation(&MAG_Cure_cameraAnimation)` — so `MAG_Cure_cameraAnimation` is shared
data, and editing it changes both spells. Second, Esuna takes
`min(target_count - 1, actionCountMinus1)`, reading **both** count fields; that is independent
evidence that `+16` and `+17` are distinct quantities (see the
[Thundara case study](../thundara-case-study/#3-the-director-iterates-actions-not-targets)).

## 5. The nested emitter — `MAG_001_CURE_Emitter_Tick` @0x8D6CC0

Phase 3 spawns this, and it is **itself a state machine** (`emitter_states[0..3]`): it plays the
cure SFX (`BdPlaySE`, `MAG001_CURE_soundId`) on its frame 0, refreshes its position and the
target model's bounding box each frame, and dispatches its own phases:

| Emitter phase | Handler | Does |
|---|---|---|
| 0 | `Emitter_State0_PlayStream` | start the heal effect stream |
| 1 | `Emitter_State1_Advance` | `++phase` |
| 2 | `Emitter_State2_ApplyHeal` | **once frame ≥ 15: `ApplyActionResultToTarget` → the HP is restored here**, then set the done flag |
| 3 | `nullsub` | idle |

**Cure's actual heal lands in the emitter at frame 15**, not in the director. The director only
orchestrates; the emitter applies the result and owns the target's bounding box. (Firaga is the
same idea — damage at director frame 48 — but Cure pushes it down into the emitter task.)

The emitter does **not** draw anything itself. Its `State0` spawns the task that does.

## 6. The helix — `MAG_001_CURE_Ring_Tick`

This is Cure's actual visual, one level below the emitter, and it is where the effect's whole
character comes from. The full tree:

```
MAG_001_CURE_Init
 └─ MAG_001_CURE_Tick                  director,  rootQueue      (0x64 × 2)
    └─ MAG_001_CURE_Emitter_Tick       emitter,   emitterQueue   (0x58 × 4)   heal lands here @frame 15
       └─ MAG_001_CURE_Ring_Tick       THE VISUAL, particleQueue1 (0x6C × 300)
          ├─ MAG_001_CURE_Sparkle_Tick particleQueue1   4/frame, frames 1–16
          ├─ MAG_001_CURE_Mote_Tick    particleQueue1   1–3/frame
          └─ MAG_005_sub_8DCC20        particleQueue2   (0x5C × 100)  2–4/frame
```

That is what the two big particle pools are for — the §2 counts of 300 and 100 are sized for these
spawn rates, not for the emitter.

### It is a helix, and it measures the target

`Ring_State0_Init` seeds every dimension from the **target's own model**. There are no hardcoded
sizes:

| Field | Value |
|---|---|
| `center_x` / `center_z` | the emitter's anchor bone 0xF1 (x, z) |
| `center_y` | `based_position_y + bounds_max_y` |
| `ring_radius` | `max(bbox width, bbox depth)`, **capped at 1024** |
| `vel_y` | `-(bbox height + 256) / 80` |

The bbox comes from `Emitter_ComputeModelBounds`, which walks **every transformed bone** of the
target each frame. Each tick then runs **4 substeps**:

```c
step   = substep + 4*frame_counter;        // 4 points per frame, continuous across frames
pos    = center;
pos_y += step * vel_y;                     // climbs steadily -> a helix, not a flat ring
angle  = (step << 7) & 0xFFF;              // 12-bit turn (4096 = 360°)
pos_x += ring_radius * sin(angle) / 4096;
pos_z += ring_radius * cos(angle) / 4096;
```

One revolution per 32 steps = **every 8 frames**, so ~2.5 turns over the 20-frame life. The total
climb is `79 × vel_y ≈ bbox height + 256` — the helix **sweeps exactly the target's full body**
plus a 256 overshoot. This is why Cure looks right on both Squall and a Grat with no per-target
data anywhere.

Its own three states: `State0_Init` (above) → `State1_WaitFrame20` (at frame 20 swap the sprite
and set a 4-frame lifetime) → `State2_EndAndUnblockDirector` (clear the director's
`emitter_spawned` → next target).

### The sprite sequences

Each particle points at an **`EffectSpriteSequence`** — a keyframed sprite/geometry blob in `.data`.
`DrawSprite` feeds the particle's **`lifetime_counter` as the frame index**, so `lifetime_limit`
doubles as "last frame of the sequence to play". Cure has five:

| Sequence | Frames | Used by |
|---|---|---|
| `MAG001_CURE_ringSprite` | 2 | the ring, during the climb |
| `MAG001_CURE_ringSpriteFadeOut` | 5 | the ring, after frame 20 |
| `MAG001_CURE_sparkleSprite` | 27 | sparkles (`lifetime_limit` 8 → only frames 0–8 play) |
| `MAG001_CURE_moteSprite` | 17 | motes (`lifetime_limit` 16) |
| `MAG001_CURE_glowSprite` | 1 | the additive glow |

That yields a detail the code hides: **the ring's billboard is static for the whole climb.**
`lifetime_counter` is only ever ticked by `Effect_LifetimeTick_Expired`, which the ring calls
exclusively from `State2` — so through all 20 frames the counter stays 0 and the ring draws
`ringSprite` frame 0. Only once `State2` starts ticking does the counter run 0→4 and play the
5-frame fade-out. (`ringSprite`'s second frame is consequently never shown, and 19 of the sparkle
sequence's 27 frames are unused.)

The format is a small header — a `0x00010524` id, four default render bytes, a frame count — then a
`frame_count`-entry table of byte offsets (terminated by `0xFFFF`) pointing at each frame's
primitive block: an `int` count (bit31 = "prepend a `0xE1` draw-mode packet"), then that many
**20-byte `EffectSpritePrim` records**, each of which becomes one textured quad (POLY_FT4):

| Offset | Field | Meaning |
|---|---|---|
| +0 / +2 | `half_width` / `half_height` | quad half-extents (×8 into GTE units) |
| +1 | `intensity` | packet RGB = caller RGB × intensity ≫ 7 |
| +3 | `gpu_code` | POLY code byte (Cure uses `0x2E` = semi-transparent textured quad) |
| +4 / +5 | `u0` / `v0` | top-left texcoord; the other corners derive from the size |
| +6 | `clut` | CLUT word, **plus** a caller-selectable row offset (see below) |
| +8 / +10 | `center_ofs_x/y` | quad centre relative to the particle position (×16) |
| +12 | `angle` | Q12 z-rotation, only when `flags & 0xC00` |
| +14 | `flags_tpage` | low 9 bits = TPAGE word; `0xC00` = enable rotation+scale; high nibble = which of the 4 params offsets the CLUT row |
| +16 / +18 | `scale_x/y` | Q12, only honoured together with the rotation flag |

Two engine tricks hide in there. The high nibble of `flags` picks one of the four header/caller
param bytes and adds it (×64) to the CLUT — **palette animation without touching the data**. And
the drawing side (`EffectSprite_EmitFramePrims`, the function previously mislabelled
`ProcessCameraFrames`) computes the OT bucket **once**, from the first visible prim, then layers the
rest of the frame's prims with a small per-prim depth bias — so a frame's quads never z-fight.

The caller-side contract of `InitEffectSequenceFromData` (the shared entry point for every
billboard effect in battle) is documented in its IDB comment. One correction that came out of the
decode: workspace offset **+28 is an RGB modulation dword** (default `0x00808080` = neutral), not a
callback — see the trap below.

> **IDA trap, the big one.** `0x808080` — neutral RGB — is a valid `.text` address, so IDA renders
> the constant as a pointer to the accidental "function" there (formerly `MAG_006_sub_808080`, now
> `FALSE_FUNC_xrefs_are_rgb_808080`). That symbol has **hundreds of xrefs and not one of them is a
> call**: damage-number colour tables, world-map fog draws, dozens of `MAG_*` effects — every one
> is the colour constant. Read any reference to it as the number `0x00808080`.

### What else it spawns and draws

- **Sparkles** — 4/frame while frame ∈ [1,16] (~64 total). Each takes a random velocity:
  `vel_x`/`vel_z` = `(rand() & 0x1F) - 16` (symmetric), `vel_y` = `(rand() & 0xF) + 16` (always
  the same sign, so they scatter in X/Z while drifting consistently in Y). 8-frame life.
- **Motes** — 1–3/frame at a random angle, radius `1.5×` the helix (same 1024 cap).
- **Glints** — 2–4/frame into the second pool, with a random ±64 spin.
- **The green wash** — see [§7](#7-the-green-wash-is-projective-texturing). It is not a tint: Cure
  hides the target from the normal renderer and draws it itself, projecting the cure texture onto
  the model like a slide projector.
- **Fade** — while frame < 20 an additive glow is drawn with `rgb = 60 - 3*frame` (60 → 0).

### Task-node field map (the heal/status framework)

The heal family stores its per-cast scratch in the task node's payload. **There are two layouts**,
sharing only the `+0..+45` prefix and diverging from +76 — the director/emitter keep the target
AABB there, the particle nodes keep sprite/lifetime/velocity. Applying one to the other is what
made this code look opaque for so long.

**Director (0x64) and emitter (0x58)** — `TaskNodeMagicHeal`; the emitter is the same layout simply
allocated 12 bytes shorter:

| Offset | Field | Meaning |
|---|---|---|
| +12 | `cast_context` | the cast context, copied down to **every** node in the tree |
| +16 | `root_director` | the director node (self-pointer on the director) |
| +20 | `bounds_source` | node holding the target AABB/anchor (self-pointer on the emitter) |
| +24 | `linked_task_to_release` | its `busy_lock` is decremented on exit |
| +36 | `frame_counter` | ++ per frame (emitter applies heal at 15) |
| +38 | `status_flags` | bit0 = finished |
| +40 | `busy_lock` | non-zero = don't finish yet |
| +41 | `state_phase` | state-machine index |
| +42 | `action_index` | **index of the action/target being played** (loop counter) |
| +48 / +64 | anchor bones 0xF1 / 0xF0 | +56..+60 is their midpoint |
| +72..+87 | target AABB | `min_x/y/z` at +72/+74/+76, `max_x/y/z` at +80/+82/+84 |
| +88 | `action_count_limit` | **action count** for the phase-4 loop |
| +92 | `tick_counter` | ++ per frame; `&1` selects the VRAM double-buffer |
| +94 | `subqueue_alive_count` | what phase 6 blocks on |
| +99 | `emitter_spawned` | `State03` sets, the ring clears, `State04` waits on |

**Ring / sparkle / mote (0x6C)** — `TaskNodeCureParticle`:

| Offset | Field | Meaning |
|---|---|---|
| +28/+30/+32 | `pos_x/y/z` | draw position, recomputed from `center` every substep |
| +66 | `spin_angle` | current 12-bit helix angle |
| +76 | `sprite_template` | pointer to the billboard template in `.data` |
| +80/+82 | `lifetime_counter` / `lifetime_limit` | also the sprite's animation frame index |
| +88/+90/+92 | `vel_x/y/z` | ring: `vel_y` is the helix climb; sparkle/mote: plain velocity |
| +96/+98/+100 | `center_x/y/z` | helix center |
| +104 | `ring_radius` | helix radius |

The pointer fields at +12/+16/+20/+24 are propagated child←parent by
`Effect_AddTaskAndInitFromCtx`. That is what lets the ring, four levels down, reach back up and
clear the director's `emitter_spawned` byte.

## 7. The green wash is projective texturing

The most interesting mechanism in the effect, and the one that is easiest to mis-read as a simple
tint. It is not a tint. **Cure takes over rendering the target model.**

`Ring_State0_Init` sets `BATTLE_ENTITY_ENTITY_FLAG_INVISIBLE` (0x4) on the target's `entity_flags`,
which hides it from the normal battle render pass for the whole life of the helix. From then on the
ring itself is responsible for drawing the target, and `Ring_State2` clears the bit again to hand
rendering back. (A ring that died without reaching State2 would strand the target invisible.)

The overlay state lives in a 248-byte context, `MAG001_CURE_overlayCtx`, built once by
`SetupTargetOverlay` and refreshed every frame. Each frame, while `status_flags & 8`:

1. **`Ring_Tick`** writes `overlayCtx.step_vec_y = ring->pos_y` and calls `SetOverlayTexturePage`
   with the ring's current position as the anchor — so both the projector's aim and its origin
   follow the helix as it climbs.
2. **`Overlay_UpdateMatrices`** copies the entity's world transform into the context and shifts the
   translation by `step_vec`.
3. **`Overlay_BuildProjectorMatrix`** builds a "slide projector" camera: the axis is
   `shifted model position − ring position`, normalised, crossed with up `(0, 4096, 0)` through the
   GTE's outer-product op to form an orthonormal basis, scaled by `scale_q12` (`0x2000` = 2.0).
4. **`Overlay_RenderModel`** draws every front-facing polygon **twice**:

| Pass | Packet | Texture | Goes to |
|---|---|---|---|
| model | `0x24`/`0x2C` opaque textured | the model's own UV/CLUT/TPage | `model_ot_cursor_ptr` |
| overlay | `0x36`/`0x3E` **semi-transparent** | the cure texture window | `overlay_ot_cursor_ptr` |

The overlay pass is where the trick lives: **its UVs are screen coordinates.** Each polygon's
vertices are re-projected through the projector matrix, the result must land inside a screen-centred
`tex_w × tex_h` window (else the overlay packet is skipped), and the UV is that screen position
remapped into the texture region. That is projective texturing — the cure texture is projected onto
the body from the ring's position, which is why the wash *slides* over the model instead of sticking
to it, and why it sweeps upward with the helix.

Both passes are depth-sorted into the same ordering table. The model redraw also handles the blob
shadow (skipped when `BATTLE_ENTITY_SHADOW_HIDDEN` is set) and re-runs the entity's animation, so
the overlay tracks the target's live pose. See
[GTE emulation layer]({{ site.baseurl }}/technical-reference/main/gte-emulation/) for the packet and
ordering-table conventions.

## 8. How to modify Cure

### Tier 1 — texture (with a big caveat)

Cure's texture is the **shared** `mag000-049.tim`, used by ~50 effects. Recolouring it restyles
Cure **and every other effect in that block**. To restyle *only* Cure you must give it a new
effect_id backed by its own loader/atlas (Recipe A in the
[Firaga case study](../firaga-case-study/#7-recipe-add-a-brand-new-spell-animation)). Contrast
Firaga, whose `mag142.tim` is dedicated and safe to edit alone.

**The green wash is the exception.** Its texture is not selected by a shared sprite template but by
raw VRAM coordinates, passed *per frame* from `Ring_Tick`:
`SetOverlayTexturePage(&overlayCtx, &ring->pos_x, 512, 384, 320, 241, 128, 128)` — a 128×128 window
at VRAM (512,384) with its CLUT at (320,241). That call site is Cure's own, so **repointing those
coordinates at a custom upload recolours the wash and nothing else**, no new effect_id required.
The tint multiplier `overlayCtx.overlay_r/g/b` (0x80 = neutral, set by `SetupTargetOverlay`) is a
second, even cheaper knob.

### Tier 2 — retiming / behaviour (hex-patch)

> **Do not patch +88 to make Cure linger.** It is the *action count* the phase-4 loop runs to, not
> a duration. Raising it makes the director spawn emitters for actions that do not exist; lowering
> it drops targets from a multi-target cast. The two fields at +42/+88 are a loop index and its
> bound — treat them as such.

The effect's real timing knobs, in the order you are most likely to want them:

- **Helix envelope:** `Ring_State0_Init` holds the two magic numbers — the `1024` radius cap and
  the `+256` height overshoot. These set how wide and how far past the head the helix goes.
- **Helix speed:** the `/80` divisor in `vel_y` sets how fast it sweeps the body; the `<< 7` in the
  angle sets the 8-frame revolution period.
- **Particle density:** the sparkle window `[1,16]` and the 4-substep loop in `Ring_Tick` give
  ~64 sparkles; the mote/glint counts are frame-range tables in their spawners.
- **Heal timing:** the heal is applied by the emitter when its `frame_counter` reaches **15**
  (`Emitter_State2_ApplyHeal`, the `>= 15` compare) — change that constant to move when the HP pops
  relative to the visual.
- **Effect length:** the ring's frame-20 threshold (`State1_WaitFrame20`) and its 4-frame lifetime
  are what end one target's helix and release the director to the next one.
- **Which phase spawns what:** `State03_SpawnEmitter` chooses the emitter task and pool —
  repoint it to spawn a different effect task.
- **Sound:** the emitter reads its SFX id from `MAG001_CURE_soundId` (0x16417C4).
- **Camera:** `MAG001_CURE_cameraAnim` (0x16417C8) is Cure's camera track (same format as any
  battle-stage camera).

Because everything scales off the target's bbox, a **larger target automatically gets a larger,
faster-climbing helix** — there is no per-target tuning to do, and none to break.

### Tier 3 — new behaviour

Same as Firaga: an FFNx DLL, but for a heal-style spell you would **reuse the shared framework**
(`Effect_AddTaskAndInitFromCtx` / `Effect_UpdateTargetPosFromBones` / `Effect_ReleaseLinkedTask`)
and supply your own phase-handler table and emitter — much less code than Firaga's from-scratch
director because the framework already does target tracking, sub-queue execution and cleanup.

## 9. Function reference (Cure)

| Address | Name | Role |
|---|---|---|
| 0x8D69E0 | `MAG_001_CURE_FL` | loader (`mag000-049.tim`, shared atlas) |
| 0x8D6A00 | `MAG_001_CURE_Init` | build 4 pools, add director, camera, upload |
| 0x8D6B30 | `MAG_001_CURE_Tick` | state-machine director |
| 0x8D6C60–0x8D84E0 | `MAG_001_CURE_State00…State09` | phase handlers (jump table) |
| 0x8D8460 | `MAG_001_CURE_State04_NextTargetLoop` | the per-action loop (phase 4 → 3) |
| 0x8D84B0 | `MAG_001_CURE_State06_WaitSubQueuesEmpty` | blocks until every sub-queue drains |
| 0x8D6CC0 | `MAG_001_CURE_Emitter_Tick` | the heal emitter (nested state machine) |
| 0x8DC610 | `MAG_001_CURE_Emitter_UpdatePos` | anchor bones 0xF0/0xF1 + midpoint |
| 0x8DC870 | `MAG_001_CURE_Emitter_ComputeModelBounds` | target AABB over every transformed bone |

The visual layer (all `TaskNodeCureParticle` nodes):

| Address | Name | Role |
|---|---|---|
| 0x8D6D80 | `MAG_001_CURE_Ring_Tick` | **the helix** — 4 substeps/frame, spawns everything below |
| 0x8D81B0 | `MAG_001_CURE_Ring_State0_Init` | seeds center/radius/`vel_y` from the target model |
| 0x8D8370 | `MAG_001_CURE_Ring_State1_WaitFrame20` | swap sprite, set 4-frame lifetime |
| 0x8D83A0 | `MAG_001_CURE_Ring_State2_EndAndUnblockDirector` | clears `emitter_spawned` → next target |
| 0x8D8080 | `MAG_001_CURE_Ring_SpawnSparkle` | 4/frame while frame ∈ [1,16] |
| 0x8D7E20 | `MAG_001_CURE_Ring_SpawnMotes` | 1–3/frame, radius 1.5× |
| 0x8D7D50 | `MAG_001_CURE_Ring_SpawnGlints` | 2–4/frame into the second pool |
| 0x8D80B0 | `MAG_001_CURE_Sparkle_Tick` (+ `_State0_RandomVelocity` 0x8D8110, `_State1_Integrate` 0x8D8160) | random-velocity sparkle |
| 0x8D7F60 | `MAG_001_CURE_Mote_Tick` (+ `_State0_RandomVelocity` 0x8D7FC0, `_State1_Integrate` 0x8D8000) | mote |
| 0x8D6F20 | `MAG_001_CURE_DrawSprite` | billboard draw from `sprite_template` |
| 0x8D6F90 | `MAG_001_CURE_DrawAdditiveGlow` | the `60 - 3*frame` fade |
| 0x8DCC20 | `Effect_Glint_Tick` | the glint (`TaskNodeCureGlint`, second pool) — see below |

Sprite sequence data (`EffectSpriteSequence`, all `.data`):

| Address | Name |
|---|---|
| 0x1641F78 | `MAG001_CURE_ringSprite` |
| 0x1641FCC | `MAG001_CURE_ringSpriteFadeOut` |
| 0x164205C | `MAG001_CURE_moteSprite` |
| 0x1642238 | `MAG001_CURE_sparkleSprite` |
| 0x1642504 | `MAG001_CURE_glowSprite` |

The green-wash overlay chain ([§7](#7-the-green-wash-is-projective-texturing)):

| Address | Name | Role |
|---|---|---|
| 0x8D8280 | `MAG_001_CURE_SetupTargetOverlay` | one-time build of `MAG001_CURE_overlayCtx` |
| 0x8D7050 | `MAG_001_CURE_SetOverlayTexturePage` | per-frame texture window + projector anchor |
| 0x8D7110 | `MAG_001_CURE_DrawTargetModelWithOverlay` | per-frame entry: matrices → projector → render |
| 0x8D7200 | `MAG_001_CURE_Overlay_UpdateMatrices` | entity transform + `step_vec` shift |
| 0x8D72C0 | `MAG_001_CURE_Overlay_BuildProjectorMatrix` | the "slide projector" camera |
| 0x8D7430 | `MAG_001_CURE_Overlay_RenderModel` | draws each polygon twice (model + projected wash) |

Despite their generic look, every function in that table has exactly one caller and is
Cure-specific. The glint is the opposite case: `Effect_Glint_Tick` is shared with the
MAG_005/021/022/040/068 effects, hence the neutral prefix.

Shared framework: `Effect_AddTaskAndInitFromCtx` (0x8DC540),
`Effect_UpdateTargetPosFromBones` (0x8DC740), `Effect_ReleaseLinkedTask` (0x8DC530);
target-measuring helpers `Effect_GetTargetBoundsRadius` (0x8DCA70),
`Effect_GetTargetBoundsHeight` (0x8DCAA0), `Effect_GetTargetBoundsMaxWorldY` (0x8DCAC0),
`Effect_GetTargetBoundsCenterWorldY` (0x8DCB80), `Effect_CopyAnchorXZFromSource` (0x8DC6E0),
`Effect_CopyMidpointFromSource` (0x8DC700), `Effect_LifetimeTick_Expired` (0x8D8040),
`Math_NormalizeVec3_Q12` (0x56BD20), `Effect_BuildMatrixFromDirAndUp` (0x8DDA50);
plus the usual `BdLink_InitTaskQueuePool` (0x508300),
`AddTaskToQueue` (0x508360), `ExecuteTaskQueue` (0x508420),
`Battle_PlayCameraAnimation` (0x5099A0), `Battle_QueueTIMUpload_GetEOF` (0x505E30),
`InitEffectSequenceFromData` (0x571C80), `BdPlaySE` (0x501330).

The geometry underneath all of it — vertex transforms, backface culling, the ordering table — is the
[GTE emulation layer]({{ site.baseurl }}/technical-reference/main/gte-emulation/).

## 10. Open questions

- ~~**Battle Y-axis sign.**~~ **Resolved** (via the [Blizzard study](../blizzard-case-study/)):
  battle world **+Y is down**. Blizzard's falling ice accelerates with *positive* `vel_y`
  (gravity), its crystal spawns at `y − 900` (above) and slams down to `ground_y − 196`, and
  Fire's rising embers use negative velocities. So `bounds_max_y` is the **feet**, the helix
  starts at the feet and sweeps **up** the body, and Cure's sparkles (positive `vel_y`) drift
  gently downward.
- **`rand()` and the 60 fps frame-hold.** The sparkle/mote/glint spawners call `rand()`, so a held
  tick re-rolls their velocities — the same class of side effect as the SFX and damage numbers
  already suppressed in
  [Magic Spell Effect Runtime](../magic-spell-effect-runtime/#the-single-per-frame-driver--one-gate-fixes-every-effect).
  Cure under the frame-hold is not verified in-game.
- **Multi-target Cure** exercises the phase-3↔4 loop far harder than a single-target cast; also not
  yet verified in-game.
- **`EffectSpriteSequence`'s header dword** is `0x00010524` in all five Cure sequences and is not
  read by `InitEffectSequenceFromData` (which starts at +4). A format id, most likely, but
  unconfirmed. The four default bytes at +4..+7 are the CLUT-row offset params selectable per prim
  (see §6) — `ringSprite` and `glowSprite` each set one non-zero.
- **Entity-slot count.** `BattleEntitySlotData` (0x1D972C0, stride 156) is **exactly 7 slots** —
  proven by `Magic_EffectEnd_ResetCameraAndEntityFlags`, whose loop walks it in 0x9C steps until it
  reaches the next global (`CAMERA_FLAG_RELATED` @0x1D97704), and
  `(0x1D97704 − 0x1D972C0) / 156 = 7` exactly. This does **not** obviously reconcile with the
  11-slot `BATTLE_SLOT_DATA` map (3 party / 5 enemies / 3 GF) in
  [Battle Slot Data](../battle-slot-data/): those are gameplay slots on a different array
  (0x1D27B10, stride 0xD0). How a gameplay slot id maps onto one of the 7 *entity/model* slots is
  not established here, and `target_entity_slot` indexes the latter.
