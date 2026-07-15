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

Knowing both patterns is enough to read essentially every regular spell. Read
[Magic Effect Anatomy & Authoring](../magic-effect-anatomy/) for the shared model; addresses are
the **2013 Steam English `FF8_EN.exe`**. Fujin shows these functions live.

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
This matters for modding (see [§6](#6-how-to-modify-cure)).

## 2. Init — `MAG_001_CURE_Init` @0x8D6A00

Unlike Firaga's two queues, the heal framework sets up **four** BdLink task pools — a root pool
plus three parallel sub-effect pools that the director ticks every frame:

| Pool | Node size × count | Role |
|---|---|---|
| `unk_277AFC0` (root) | 0x64 × 2 | holds the director task |
| `stru_278A228` | 0x58 × 4 | emitters (the sparkle/heal effect) |
| `stru_277BF70` | 0x6C × 300 | particles |
| `stru_278C788` | 0x5C × 100 | particles |

It adds the director with `Effect_AddTaskAndInitFromCtx` (the shared "add task + copy target
info from the cast context" helper), plays a hardcoded camera (`unk_16417C8`), uploads the
texture, initialises three VRAM cursors, and returns the root queue.

## 3. The state-machine director — `MAG_001_CURE_Tick` @0x8D6B30

```c
int MAG_001_CURE_Tick(int task_node) {
  qmemcpy(&unk_2793E58, &BD_LINK_TASK_HEADER_CAMERA.data, 0x20u);  // snapshot camera
  v4[0]  = MAG_001_CURE_State00_Advance;
  v4[1]  = MAG_001_CURE_State01_Advance;
  v4[2]  = MAG_001_CURE_State02_WaitUnlocked;
  v4[3]  = MAG_001_CURE_State03_SpawnEmitter;
  v4[4]  = MAG_001_CURE_State04_HoldLoop;
  v4[5]  = MAG_001_CURE_State05_Advance;
  v4[6]  = MAG_001_CURE_State06;
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
| 3 | `State03_SpawnEmitter` | spawns `MAG_001_CURE_Emitter_Tick` into the emitter pool, sets a flag, `++phase` |
| 4 | `State04_HoldLoop` | counts up to a limit, ping-pongs the phase back — a **timed hold** |
| 5 | `State05_Advance` | `++phase` |
| 6–8 | `State06/07/08` | pacers |
| 9 | `State09_Finish` | sets the "finished" flag (`+38 |= 1`), `++phase` |
| 10 | `nullsub_959` | no-op (idle until the queues drain) |

So Cure's timeline is: pace in → **spawn the heal emitter** (phase 3) → **hold** while it plays
(phase 4) → mark finished (phase 9) → idle until the sub-queues empty → director releases its
linked task and dies.

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

**This is the key finding: Cure's actual heal lands in the emitter at frame 15**, not in the
director. The director only orchestrates timing; the emitter both draws the sparkle and applies
the result. (Firaga is the same idea — damage at director frame 48 — but Cure pushes it down into
the emitter task.) This is also why the heal nests deeper than Firaga: `init → director →
State03 → emitter → emitter states`, which is why the export walker follows up to 5 levels.

### Task-node field map (the heal/status framework)

The heal family stores its per-cast scratch in the task node's payload (0x64 bytes). The
IDB documents it in full on `MAG_001_CURE_Tick`; the fields that matter for modding:

| Offset | Field | Meaning |
|---|---|---|
| +12 | `action_ctx` | per-target action/target descriptor |
| +36 | `frame_counter` | ++ per frame (emitter applies heal at 15) |
| +38 | `done_flags` | bit0 = finished |
| +40 | `lock` | non-zero = don't finish yet |
| +41 | `phase` | state-machine index |
| +88 | `hold_limit` | `State04_HoldLoop` duration |
| +92 | `tick_counter` | ++ per frame; `&1` selects the VRAM double-buffer |
| +99 | `emitter_spawned` | `State03` sets, `State04` waits on |

## 6. How to modify Cure

### Tier 1 — texture (with a big caveat)

Cure's texture is the **shared** `mag000-049.tim`, used by ~50 effects. Recolouring it restyles
Cure **and every other effect in that block**. To restyle *only* Cure you must give it a new
effect_id backed by its own loader/atlas (Recipe A in the
[Firaga case study](../firaga-case-study/#7-recipe-add-a-brand-new-spell-animation)). Contrast
Firaga, whose `mag142.tim` is dedicated and safe to edit alone.

### Tier 2 — retiming / behaviour (hex-patch)

- **Phase pacing:** the phase handlers are where timing lives. `State04_HoldLoop` holds the
  effect for a fixed count (`hold_limit`, node +88) — patch that to make Cure linger. The pacer
  phases (`++phase`) can be added/removed to shift the emitter's start.
- **Heal timing:** the heal itself is applied by the emitter when its `frame_counter` reaches
  **15** (`Emitter_State2_ApplyHeal`, the `>= 15` compare) — change that constant to move when
  the HP pops relative to the sparkle.
- **Which phase spawns what:** `State03_SpawnEmitter` chooses the emitter task and pool —
  repoint it to spawn a different effect task.
- **Sound:** the emitter reads its SFX id from `MAG001_CURE_soundId` (0x16417C4).
- **Camera:** `MAG001_CURE_cameraAnim` (0x16417C8) is Cure's camera track (same format as any
  battle-stage camera).

### Tier 3 — new behaviour

Same as Firaga: an FFNx DLL, but for a heal-style spell you would **reuse the shared framework**
(`Effect_AddTaskAndInitFromCtx` / `Effect_UpdateTargetPosFromBones` / `Effect_ReleaseLinkedTask`)
and supply your own phase-handler table and emitter — much less code than Firaga's from-scratch
director because the framework already does target tracking, sub-queue execution and cleanup.

## 7. Function reference (Cure)

| Address | Name | Role |
|---|---|---|
| 0x8D69E0 | `MAG_001_CURE_FL` | loader (`mag000-049.tim`, shared atlas) |
| 0x8D6A00 | `MAG_001_CURE_Init` | build 4 pools, add director, camera, upload |
| 0x8D6B30 | `MAG_001_CURE_Tick` | state-machine director |
| 0x8D6C60–0x8D84E0 | `MAG_001_CURE_State00…State09` | phase handlers (jump table) |
| 0x8D6CC0 | `MAG_001_CURE_Emitter_Tick` | the heal emitter (nested state machine) |

Shared framework: `Effect_AddTaskAndInitFromCtx` (0x8DC540),
`Effect_UpdateTargetPosFromBones` (0x8DC740), `Effect_ReleaseLinkedTask` (0x8DC530),
`Effect_AddTaskAndInitFromCtx`; plus the usual `BdLink_InitTaskQueuePool` (0x508300),
`AddTaskToQueue` (0x508360), `ExecuteTaskQueue` (0x508420),
`Battle_PlayCameraAnimation` (0x5099A0), `Battle_QueueTIMUpload_GetEOF` (0x505E30),
`InitEffectSequenceFromData` (0x571C80), `BdPlaySE` (0x501330).
