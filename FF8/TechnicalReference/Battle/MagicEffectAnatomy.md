---
layout: default
parent: Battle
title: Magic Effect Anatomy & Authoring
permalink: /technical-reference/battle/magic-effect-anatomy/
---

Full anatomy of a **magic spell animation** (particles, camera, sound, damage timing) as
implemented in the 2013 Steam EN exe, reverse-engineered from `FF8_EN.exe` — with the goal of
**modifying existing effects or creating new ones** (e.g. a brand-new "Wind Maker" spell).
Complements [Magic Spell Effect Runtime](../magic-spell-effect-runtime/) (dispatch + 60 fps
timing) and [Mag File Format](../mag-file-format/) (file layout).

1. TOC
{:toc}

## The one-sentence summary

A spell animation is **not data** — it is a **per-spell C function compiled into the exe**
(originally one `.cpp` per spell in `C:\FF8\Battle\aoy\` — the debug strings still name
`dav_aoy.cpp`). The only *file* a regular spell loads is its **TIM texture atlas**
(`\FF8\Data\Magic\magNNN.tim`, in `magic.fs`). Geometry (billboards/meshes), camera tracks,
and sound definitions are **hardcoded in the exe's `.data` section**; motion, spawn timing,
and particle behaviour are **procedural code** driven by per-frame counters and `rand()`.

## Big picture

```
kernel.bin magic entry +0x04 (effect_id) ─▶ action task +6
                                                 │
              Magic_GetIDLoad(effect_id) @0x50AF20  (idx = effect_id − 1, 0..399)
                    │
                    ├─ Magic_ClearMemoryForTex @0x571870      free previous spell's allocs
                    ├─ MagicList_TextureLoad[idx]  (MAG_NNN_*_FL)  → IO_GetFile_MAGIC("magNNN.tim")
                    └─ MagicList_Logic[idx]        (MAG_NNN_*)     → stored in MAGIC_EFFECT_LOGIC_CALLBACK
                                                 │
     BattleActionSequence_Tick_MagicCast @0x50A9A0 (case 4)  calls it ONCE:
     C3_28_GF_data_pointer = MAG_NNN_*(&RELATED_SLOT_ID_ATTACKER)
                                                 │
     every battle frame @0x50093A:  ExecuteTaskQueue(C3_28_GF_data_pointer)
                    │                            (runs Init-created task tree)
                    └─ returns 0 (all tasks done) → pointer cleared → effect over
```

Both dispatch tables live in `.data` and hold **400 slots** each:

| Global | Address | Content |
|---|---|---|
| `MagicList_Logic` | 0xC81774 | init function per effect_id (`MAG_NNN_*`); NULL = "non existent magic ID" |
| `MagicList_TextureLoad` | 0xC81DB8 | texture loader per effect_id (`MAG_NNN_*_FL`); may be NULL |

### Full table census (dumped from 0xC81774 / 0xC81DB8)

- **Used slots: effect_id 1–223 and 226–345.**
- **Free slots: 224, 225, and 346–400** (both pointers NULL) — these are the slots a new
  custom spell can claim without displacing anything.
- Effect_ids **226–345 were previously undocumented**: 120 handler pairs that were not even
  defined as functions in the community IDB. They are now defined and named
  `MAG_226_UNKNOWN` … `MAG_345_UNKNOWN` (+`_FL`). By their code patterns they fall into the
  same three families as the known ones (tiny stub → shared cinematic loader; GF-summon
  style `FL 0x22/main 0x5D` pairs; full standalone inits) and are most likely **monster
  attacks and story-scene cinematics** (Lunatic Pandora, sorceress scenes, …).
  Identifying each one (cast them in-game / cross-reference monster attack data) is open work.
- ⚠ **Name corrections**: the table is ground truth, and it revealed that several older IDB
  main-function names were assigned to the wrong address (`_FL` names were correct; the
  mains were shifted). Fixed so far: slot 51 (`MAG_051_HIPOTION` @0x81C800), slots 197/198
  (SHOT Armor/Hyper mains @0x5AED30/0x5AA3E0), slot 327 (0x58D760 was wrongly named
  `MAG_078_MIGHTY_GUARD`; real slot-78 main is 0x7BE2D0). **Rule for tools: always resolve
  a spell's functions through the tables, never trust a name's number.** Several mains in
  the 34–98 range still carry shifted names (e.g. 0x7E4B00 is named `MAG_034_PAIN` but is
  slot 62's main).

## The BdLink task system

All effect runtime behaviour is built on a tiny cooperative-task engine ("BdLinkTask" per
its debug string):

| Function | Address | Role |
|---|---|---|
| `BdLink_InitTaskQueuePool` | 0x508300 | binds a queue header to a static node pool (node size + count), zeroes it |
| `AddTaskToQueue` | 0x508360 | grabs a free node from the pool, appends it, sets its tick function |
| `ExecuteTaskQueue` | 0x508420 | ticks every node once; **return & 2 → node removed**; returns surviving-node count |
| `Effect_AddTaskAndInitFromCtx` | 0x8DC540 | AddTaskToQueue + zero the payload + copy target/entity info from a cast context |

A node is a 12-byte header (`next`, `task_func`, `flags/sequence_id`) followed by a
**free-form payload** the spell code uses however it wants — typically frame counters,
positions, velocities, scale, per-target index. Task functions return `0` to stay alive and
`2` to self-destruct. When *every* node of the spell's root queue has self-destructed, the
effect is finished.

## The cast context — the one argument every init receives

Every one of the 343 effect inits has the **same signature**, and it is not a guess: they are all
called through one function-pointer table, so the type is fixed by construction.

```c
TaskQueueExample *__cdecl MAG_nnn_Init(MagicCastContext *cast_context);
```

The argument is **`&g_MagicCastContext` (0x1D99A78)** — a single **global**, not an allocation.
There is only ever one cast in flight, so the engine reuses one struct:

```c
C3_28_GF_data_pointer = MAGIC_EFFECT_LOGIC_CALLBACK(&g_MagicCastContext);
```

It is filled in by **`BattleActionSequence_BuildMagicCastContext` (0x50AFC0)**, called by every cast
path immediately before the init — `_MagicEffect` (0x50B190) case 3, `_MagicCast_Simple` (0x50B0C0),
`_GF_Cinematic` (0x50B2A0), `sub_50BDC0`, `sub_50BEE0`.

| Offset | Field | Type | Meaning |
|---|---|---|---|
| +0 | `attacker_slot` | `u8` | `BATTLE_TASK_68_DATA->slotIdAttacker`. Effects use it as `&BattleEntitySlotData[attacker_slot]` (stride 156) |
| +1 | `flags` | `MagicCastFlags` | bit0 = **suppress camera track + TIM upload** (below) |
| +2 | `target_slot_mask` | `u16` | `LINKED_TARGET_SLOT_ID_0` — a **bitmask** over slots, tested as `(1 << i) & mask` |
| +4 | `action_data` | `BattleActionTaskData *` | `= BATTLE_TASK_68_DATA_ADDR`. **The payload** — targets, counts, damage |
| +8 | `sequence_mode` | `u8` | **IN:** sub-command for re-entrant effects (Shot, Duel). Derived from `action_data->word_1D280C8` (`+2`, or 8 for the 0xFFFC/0xFFFA cases) |
| +9 | `done_flag` | `u8` | **OUT:** zeroed before the init; **the effect writes 1** to say it has finished, and the action sequence ends |
| +10 | `sequence_submode` | `u8` | `0`, or `unk6 − 5` |
| +11 | `unknown_11` | `u8` | written 0, never read |

**The context is a bidirectional mailbox, not just an input.** For ordinary spells it is
write-once-then-read: the engine fills it, the init reads `+0/+1/+4`, done. But the two re-entrant
effects use it as a channel in both directions — `sequence_mode` in, `done_flag` out (§
[Duel](#duel--the-same-trick-as-an-input-channel)).

**Most effects read only `+0`, `+1` and `+4`** — who cast it, whether to play the cinematics, and a
pointer to the action data. But `+8` (`sequence_mode`) is **not** merely bookkeeping: the
[Shot family](#the-shot-family--a-re-entrant-init) branches its entire setup on it.

> **A trap when checking this.** Asking IDA for cross-references to `g_MagicCastContext.sequence_mode`
> returns only battle-sequence functions, which makes it *look* like no effect reads it. That is an
> artifact: effects typically **stash the context pointer into a private global** in the init and
> dereference it later (`*(ptr + 8)`), which no xref on the global will ever catch. Field usage must
> be judged from the effects' own stashed pointers, not from xrefs to the global.

### `flags` bit 0 — what a "simple" cast is

Every init ends with the same gate:

```c
if ( (cast_context->flags & MAGICCAST_FLAG_NO_CAMERA_OR_TIM) == 0 ) {
    Battle_PlayCameraAnimation(&MAGnnn_cameraAnim);
    Battle_QueueTIMUpload_GetEOF(MAGnnn_timBuffer);
}
```

Who sets it settles the meaning: **`BattleActionSequence_Tick_MagicCast_Simple` sets it**
(`byte_1D99A79 |= 1` @0x50B155) right after building the context, whereas the full `_MagicEffect`
path leaves it clear. So bit 0 is what makes a "simple" cast bare — the effect plays its particles
but skips its camera track and does not re-upload its texture. This is the single most useful bit in
the struct for modding: it is the engine's own switch for *"this spell, minus the cinematics."*

### Reaching the targets

Everything an effect needs about *what it is hitting* is behind `action_data`. Note the two count
fields are **different quantities** and both are live — see the
[Thundara case study](../thundara-case-study/#3-the-director-iterates-actions-not-targets):

| Path | Meaning |
|---|---|
| `action_data[0].target_count` (+16) | number of targets of an action; iterate `targetData[0..n-1]`, **stride 24** |
| `action_data[0].actionCountMinus1` (+17) | number of actions (hits); iterate `action_data[0..n]`, **stride 20** |

Both idioms occur in the wild: Fire and the GF summons loop targets; Thundara loops actions and
takes each action's first target only.

### The Shot family — a re-entrant init

There are exactly **eight 40-byte inits** in the dispatch table — the smallest by a wide margin —
and they are precisely Irvine's **Shot** limit break (ids **188, 192–198**). Nothing else in the
table is that small, and the reason is a dispatch shape unique to this family.

Their init does almost nothing: it **stashes the context into globals and delegates**.

```c
TaskQueueExample *__cdecl MAG_188_SHOT_NORMAL_SHOT_Init(MagicCastContext *cast_context) {
    MAG_188_texBuffer   = Magic_TextureOFF_ToEAX1();
    MAG_188_castCtx     = cast_context;              // stash the pointer
    MAG_188_attackerSlot = cast_context->attacker_slot;
    MAG_188_SHOT_Setup_BySequenceMode();             // no args — reads the globals
    return &MAG_188_queueRootAndShots;
}
```

Note there is **no camera/TIM gate** here, unlike every other init. That is the tell: the real setup
(`MAG_188_SHOT_Setup_BySequenceMode`, 0x5BE370) branches on **`castCtx->sequence_mode` (+8)**:

| `sequence_mode` | Action |
|---|---|
| 0 | **full init** — pools (`0x10×4` root, `0x24×100` twice), root task, effect task, zero the two 900-entry tables, `resetSomeCameraData()`, `Battle_QueueTIMUpload_GetEOF` |
| 1 | add task `MAG_188_sub_5BF100` |
| 2 | **fire one shot** — spawn `MAG_188_sub_5BE4D0`, `seq_id = shotCounter % 100`, target from `castCtx->action_data->targetData->TargetSlotId`, cycle `0..2` |
| else | `mode − 2` |

So **the Shot effect entry is invoked many times per limit break** — once to build, then once per
shot — whereas every other effect's init runs exactly once per cast. The 40-byte wrapper exists
because it has to be cheap and re-entrant; all the state lives in globals between invocations.

`sequence_mode` is *not* set by `BattleActionSequence_BuildMagicCastContext`. Its writers are
`BattleActionSequence_Tick_MagicCast` (0x50AA4D) and `BattleActionSequence_Tick_Duel` (0x50BDC0).
Shot has its own re-entry handler, **`BattleActionSequence_Tick_Shot` (0x50BEE0)**, dispatched for
command types **`0xED` "Shot on hit"** and **`0xEE` "Shot time expire"**.

### Duel — the same trick, as an input channel

Zell's **Duel** (effect **274**, command type **`0xF1`**) is the most interactive effect in the game,
and it reuses the Shot mechanism for something rather different: **live player input**.

The player enters a button combo; the battle code raises a `0xF1` action;
`BattleActionSequence_Tick_Duel` (0x50BDC0) sets `sequence_mode` and re-invokes the init — which
builds **nothing**. It just latches the move and bails:

```c
TaskQueueExample *__cdecl MAG_274_DUEL_Init(MagicCastContext *cast_context) {
    if ( cast_context->sequence_mode ) {                       // re-entry: a move was entered
        MAG274_DUEL_pendingMoveId = cast_context->sequence_mode;
        MAG274_DUEL_moveChanged   = 1;
        return 0;                                              // no queue!
    }
    ... /* first call: build pools, root task, stash ctx */
}
```

Returning **0** would normally be fatal — the `_MagicEffect` path assigns the return straight to
`C3_28_GF_data_pointer`, so a NULL would end the effect. It is safe here only because
`_Tick_Duel` **discards the return value**. That is the structural signature of a re-entry path.

`MAG_274_DUEL_MoveTask` (0x689AC0) then latches `pendingMoveId` and switches on it — one handler per
move, with the finisher inline:

| `sequence_mode` | Handler |
|---|---|
| 0 | no move pending → `castCtx->done_flag = 1` |
| 2–6 | `MAG_274_DUEL_Move2_Tick` … `Move6_Tick` (0x68A050, 0x68B2F0, 0x68B700, 0x68B950, 0x68C7B0) |
| 7 | `MAG_274_sub_68CA60` |
| 8 | **finisher (inline)** — `ApplyActionResultToTarget`, restore the attacker's saved position/rotation, return 2 |

Mode = `action_data->word_1D280C8 + 2` for combo ids 0–5 → moves 2–7; and the sentinels
**`0xFFFC` / `0xFFFA` map to mode 8**, i.e. those two values *are* the "finish the Duel" signal
(time expired / final blow). Per-move duration comes from the table `MAG274_DUEL_moveDurations`
(0x110E3E0); per-move camera from `BS_GetCameraAnimationPointer(..., comData[145] + 16*(move−2))`.

The return path completes the picture: the move task writes `castCtx->done_flag = 1`, and
`_Tick_Duel` polls `byte_1D99A81 == 1` and ends the action. **That is the whole Duel loop — input in
via `sequence_mode`, completion out via `done_flag`, both through the shared cast context.**

> A by-product: the odd `commandType == 0xF0` branch at the top of
> `BattleActionSequence_BuildMagicCastContext` — which scans `BattleEntitySlotData` for
> `COM_ID_RINOA` — explains itself once you have the command list. `0xF0` is **Angelo Automove**,
> whose attacker is Rinoa, so her slot has to be found rather than read from the action.

## Anatomy of one spell — Firaga (effect_id 143, `mag142.tim`)

All of the following is per-spell code/static data; every other spell follows the same
pattern with different constants. For the full frame-by-frame walkthrough of this spell —
every task, every particle, the data block, and concrete edit recipes — see the dedicated
[Case study: Firaga animation](../firaga-case-study/). For the other archetype (a **state
machine**, used by the heal/status family), see [Case study: Cure animation](../cure-case-study/).

### 1. Texture loader — `MAG_143_FIRAGA_FL` @0x61BFC0

```c
MAG143_timFilePtr = IO_GetFile_MAGIC("mag142.tim");
```
`IO_GetFile_MAGIC` (0x571B80) → `Magic_LoadTexture_IO_GetsFile` (0x571900) reads
`\FF8\Data\Magic\<name>` through the virtual archive (magic.fs), allocates a buffer, and
registers it in `MAGIC_ALLOC_PTRS[MAGIC_ALLOC_COUNT++]` (0x21DFAC0 / 0x21DFABC, max 256) so
`Magic_ClearMemoryForTex` can free everything when the next spell loads.

### 2. Init — `MAG_143_FIRAGA` @0x61BFE0 (called once per cast)

- Saves the cast context: `MAG143_castContextPtr` = arg (attacker slot, flags, target list).
- `BdLink_InitTaskQueuePool` on **two private static queues**:
  root queue (1 × 0x10 node) and effect queue (100 × 0x24 nodes) — `MAG143_effectQueues`.
- Adds `MAG_143_FIRAGA_RootTask_RunEffectQueue` to the root queue and
  `MAG_143_FIRAGA_Director_Tick` to the effect queue.
- Unless "no camera" flag (cast ctx +1 bit0): `Battle_PlayCameraAnimation(&MAG143_cameraAnimData)`
  — a **keyframed camera track hardcoded in `.data`** (0xDD9A4C) — and
  `Battle_QueueTIMUpload_GetEOF(MAG143_timFilePtr)` which queues a type-1 command in the
  32-slot render command buffer (`g_command_bffer` 0x1D98220) to upload the TIM to VRAM.
- Returns the root queue pointer → becomes `C3_28_GF_data_pointer`.

### 3. Root task @0x61CDA0

Runs every frame: flips the **double-buffered GPU packet cursor**
(`MAG143_primBufferCursor = MAG143_primBufferBase [+ 0x10000]` on odd frames), then
`ExecuteTaskQueue(effect queue)`; self-destructs when the effect queue is empty.

### 4. Director task @0x61C0A0 — the spell's timeline

One node whose payload word is a **frame counter (0→60)**. Each frame it checks the counter
and spawns/does things:

| Frame | Action |
|---|---|
| 0 | capture target effect position (`GetDefaultEffectPosition`, avg of bone 0xF0/0xF1) |
| 1 | 3D sound: `BdPlaySE3D(&MAG143_soundDef, 0, pos)` (sound def in `.data`) |
| 1–14 | spawn **spark particles** (random unit velocity via cross-product trick, life 20 f) |
| 4 | spawn **target fireball** (billboard scaling up every frame) |
| 32 | `au_re_BdLinkTask_6(0,1,2,255)` — flash begin |
| 33 | spawn **burst** + a **flame swirl pair** (one rising, one sinking, random spin) |
| 36–48 | spawn 3 **area flames** per frame around the target, clamped near ground height |
| 44 | multi-target: queue a new Director node for the **next target** |
| 48 | `ApplyActionResultToTarget` @0x506690 — **damage numbers / HP change happen here** |
| 52–60 | `Effect_SetScreenFlash((60−t)<<8, color)` — fade the screen flash out |
| >60 | return 2 → director dies; when last particles die, effect ends |

### 5. Particle tick tasks

E.g. `MAG_143_FIRAGA_SparkParticle_Tick` (see [IDB names applied](#idb-names-applied) below), each frame:

1. Build a rotation from stored axis/angle (`BuildAxisAngleRotationMatrix` @0x5714F0 —
   Rodrigues, 4096 = 1.0 fixed point), scale it, compose with the battle camera matrix
   (`ComposeAffineTransform` @0x56C2F0).
2. `Field_Alloc(88)` a render header: `+0` prim model ptr, `+8/9/10` RGB tint, `+12`
   colour/alpha param, `+28` blend flags (48 / 240 observed).
3. `Effect_RenderPrimModel` @0x572200 — transforms the **prim model** (PSX-style section
   list compiled into `.data`, e.g. `MAG143_primModel_Spark` @0xDDCE48), clips, and emits GPU
   packets at `MAG143_primBufferCursor`. Sections of other primitive types are handled by
   0x572500/0x572730/0x572950/0x572BE0/0x572DE0/0x573050/0x573290.
4. Advance state (position += velocity, counter++), return 2 when life expires.

**Drawing happens inside the tick** — there is no separate render pass for effects (this is
why the 60 fps frame-skip gate flickers; see
[Magic Spell Effect Runtime](../magic-spell-effect-runtime/)).

## Shared helper library (the "effect SDK" inside the exe)

| Function | Address | Purpose |
|---|---|---|
| `GetEffectSpawnPosition` | 0x502170 | entity + bone code → world pos (codes ≥0xF0 are special anchors) |
| `GetDefaultEffectPosition` | 0x571400 | midpoint of anchors 0xF0/0xF1 + ground rotation |
| `Battle_PlayCameraAnimation` | 0x5099A0 | play a keyframed camera track (data ptr) |
| `Battle_QueueTIMUpload_GetEOF` | 0x505E30 | queue TIM VRAM upload, return end-of-TIM ptr |
| `Effect_SetScreenFlash` | 0x5713E0 | full-screen tint/flash (intensity, packed colour) |
| `BdPlaySE3D` | 0x5013A0 | positional sound effect from a `.data` sound def |
| `ApplyActionResultToTarget` | 0x506690 | apply damage/heal + spawn damage numbers |
| `Effect_RenderPrimModel` | 0x572200 | draw a prim model with a transform + tint |
| `BuildAxisAngleRotationMatrix` | 0x5714F0 | axis-angle → 3x3 fixed-point matrix |
| `GetRotationBetweenVectors_AxisAngle` | 0x571480 | angle + normalized axis between two vectors |
| `NormalizeVectorToFixedPoint` / `FixedPointCrossProduct` | 0x56BC50 / 0x56BBF0 | 4096-based vector math |
| `computeSin` / `computeCosine` | 0x56D130 / 0x56D100 | game-angle (0..4095) trig |
| `Field_Alloc` / `Field_Free` | 0x5082B0 / 0x5082D0 | per-frame scratch allocator (render headers) |
| `Magic_LoadTexture_IO_GetsFile` | 0x571900 | read any file from `\FF8\Data\Magic\` |
| `Magic_ClearMemoryForTex` | 0x571870 | free all `MAGIC_ALLOC_PTRS` allocations |
| `InitEffectSequenceFromData` | 0x571C80 | data-driven sub-effect sequences (AnimSeq 99/B0/B1/B4/A5 path) |

## Where everything lives

| Piece | Location | Moddable without code? |
|---|---|---|
| Texture atlas | `magic.fs` → `magNNN.tim` (N = effect_id − 1) | **Yes** — swap the TIM |
| Effect logic (timing, particle counts, motion) | `.text` per-spell functions | No — x86 code |
| Prim models (billboards/meshes) | `.data` (e.g. 0xDDA740–0xDDCE48 for Firaga) | Hex-editable, format = prim section list |
| Camera track | `.data` (e.g. 0xDD9A4C) | Hex-editable keyframes |
| Sound def | `.data` (e.g. 0xDDD8F0) | Hex-editable |
| Dispatch | `MagicList_Logic` / `MagicList_TextureLoad` tables in `.data` | **Yes — patch a pointer** |
| Which effect a spell uses | kernel.bin magic entry +0x04 | **Yes** — kernel edit |

## Tier-2 data formats

### Effect prim model (the billboards/meshes drawn by `Effect_RenderPrimModel`)

Verified against `MAG143_primModel_Spark` (0xDDCE48) and the `Effect_RenderPrimModel` renderer:

| Offset | Type | Meaning |
|---|---|---|
| +0x00 | u32 | offset from model base to the **section list** (0x100 in the spark model) |
| +0x04 | u32 | vertex count (0x1F = 31 in the spark model) |
| +0x08 | SVECTOR[] | vertices: `s16 x, y, z, pad` (8 bytes each) |
| +*(+0) | sections | 8 consecutive sections, one per primitive type |

Each section starts with a `u32 count` (0 = section absent, cursor just skips the u32).
The first section (flat triangles, handled inline by 0x572200) has **12-byte entries**:
`u32 gpu_packet_code` (PSX GPU command word: mode + RGB; bit `0x2000000` = semi-transparency,
forced on/off by render-header flags 1/4), then `u16 idx0, idx1, idx2` — vertex indices
**pre-multiplied ×2** (the renderer computes `vertex_base + 4*idx`, vertices are 8 bytes),
then 2 pad bytes. The seven remaining section types are parsed by 0x572500, 0x572730,
0x572950, 0x572BE0, 0x572DE0, 0x573050, 0x573290 (quads / textured variants / lines —
decompile the one you need; same count-prefixed layout, different entry sizes).

The 88-byte render header passed to `Effect_RenderPrimModel` (built per draw with
`Field_Alloc(88)`): +0 model ptr, +4 (auto) vertex ptr, +8/9/10 RGB tint, +12 colour/alpha
parameter, +28 flags (observed 48 and 240; bit 0x40 enables the +12 parameter path),
+32 (auto) section cursor, +36 depth, +44 OT index.

### Camera track

The blob each spell passes to `Battle_PlayCameraAnimation` is the **same format as the
battle-stage camera data**: a small header with two relative offsets (camera *sequence*
byte-code + camera *animation collection* keyframes) — fully documented in
[Camera sequence](../model-sections/camera-sequence/). The spell versions are simply
private copies embedded in `.data` (Firaga's is `MAG143_cameraAnimData` @0xDD9A4C, header
`02 00 08 00 44 01 48 0B …`). A Tier-2 tool can reuse the `.X`-file camera tooling on
these blobs directly.

### Sound definition

`BdPlaySE3D(&soundDef, attr, pos)` reads a **u32 sound code** at +0 of the def
(Firaga: 0x00049418 @0xDDD8F0) and routes it to the 3D sound path
(`sub_46B2E0`) or, without 3D capability, `PlayWorldSound(code, attr, panFromX, 0x7F)`.
The def is just that one u32; exact encoding of the code (bank/index split) is open.

### Worked patch map — Firaga director timeline constants

For a Tier-2 "retime this spell" feature, these are the code addresses of the hardcoded
constants inside `MAG_143_FIRAGA_Director_Tick` (compare-immediates, patchable in place):

| Constant | Meaning | Code address |
|---|---|---|
| 1..14 | spark-spawn frame window | 0x61C0FB–0x61C10F |
| /6+1 | sparks spawned per frame | 0x61C124 |
| 4 | target fireball spawn frame | 0x61C2B2 |
| 32 | screen-flash start frame | 0x61C2F8 |
| 33 | burst + flame-swirl spawn frame | 0x61C314 / 0x61C402 |
| 36..48 | area-flame window (3/frame) | 0x61C451 |
| 44 | chain to next target | 0x61C597 |
| 48 | **damage applied** (`ApplyActionResultToTarget`) | 0x61C574 |
| 60 | director lifetime | 0x61C679 |
| 20 / 24 | spark / swirl particle lifetimes | 0x61CD8D / 0x61CB02 |

Every other spell follows the same pattern; harvesting its map is the same exercise on its
director function (start from the table, not from names).

## Read-only pseudocode for the tool

The repo script `Fujin/ResearchScript/dump_magic_effects.py` (FF8UltimateEditor) runs inside IDA
on the FF8_EN.exe database and exports `magic_effects.json`: for every effect_id, the
handler addresses, the files its `_FL` loads, and the **Hex-Rays pseudocode of the init +
its spell-local sub-functions** (director, particle ticks, two call levels deep). That JSON
is what the tool should ship for its "view spell logic (read-only)" panel, plus
`magic_effects_table.md` as a human-readable index.

## Creating a new spell animation ("Wind Maker") — tool roadmap

Because effects are code, a "magic animation editor" has three realistic tiers:

**Tier 1 — remix (no code injection).** Point the new spell's kernel entry +0x04 at an
existing effect (e.g. Tornado = 146, Aero = 118) and swap/recolour its `magNNN.tim`. The
motion stays, the look changes. A tool can already do: effect_id picker + TIM
import/export/recolour + kernel patch.

**Tier 2 — data patching.** Keep an existing handler but edit its `.data` assets: prim
model vertices/UVs, camera track, sound def, and (with a table of per-spell constant
addresses) patch immediates in the director (frame timings, particle counts, scales). Needs
per-spell offset maps harvested from the IDB.

**Tier 3 — true new effect (code).** Ship a DLL (FFNx / `AF3DN.P` — Hext cannot host new
code on the 2013 exe, see the runtime page) that:

1. Registers custom `WindMaker_Init` / `WindMaker_FL` into a **free slot** of
   `MagicList_Logic` / `MagicList_TextureLoad` (400 slots; many are NULL), or overwrites a
   junk slot like 44 (`MAG_044_JUNK`).
2. `WindMaker_FL` loads a new `magNNN.tim` (drop the file into `magic.fs` — the loader takes
   any filename) via `IO_GetFile_MAGIC`.
3. `WindMaker_Init` reproduces the standard pattern: init two task pools, add a root task +
   a director, optionally `Battle_PlayCameraAnimation` (reuse any existing track), queue the
   TIM upload, return the root queue.
4. Director + particle ticks call the **shared helpers above by address** — spawn positions,
   matrix math, `Effect_RenderPrimModel` with custom prim models (can live in the DLL's own
   memory; the renderer only needs a pointer), screen flash, `BdPlaySE3D`, and
   `ApplyActionResultToTarget` at the "hit" frame.
5. Set the new spell's kernel +0x04 to the chosen effect_id.

The highest-leverage tool design: implement **one generic, data-driven director** in the DLL
(timeline of `{frame, action, params}` records + emitter descriptions loaded from a mod
file), so creating "Wind Maker" becomes writing a timeline file + a TIM — no compiler needed
by end users.

## IDB names applied (this study)

Functions: `BdLink_InitTaskQueuePool` (0x508300, ex-`BS_Memset`), `Effect_AddTaskAndInitFromCtx`
(0x8DC540), `BattleActionSequence_Tick_MagicCast_Simple` (0x50B0C0),
`Magic_IsEffectOrCameraStillRunning` (0x50AE80), `Magic_EffectEnd_ResetCameraAndEntityFlags`
(0x50AED0), `Effect_SetScreenFlash` (0x5713E0), `BuildAxisAngleRotationMatrix` (0x5714F0),
`GetRotationBetweenVectors_AxisAngle` (0x571480), `Effect_RenderPrimModel` (0x572200),
`Battle_QueueTIMUpload_GetEOF` (0x505E30, ex-`GetTextureEOF`), and the Firaga family
`MAG_143_FIRAGA_RootTask_RunEffectQueue` / `_Director_Tick` / `_SparkParticle_Tick` /
`_TargetFireball_Tick` / `_FlameSwirl_Tick` / `_Burst_Tick` / `_AreaFlame_Tick`
(0x61CDA0 / 0x61C0A0 / 0x61CBB0 / 0x61CB10 / 0x61C9C0 / 0x61C870 / 0x61C6B0).

Re-entrant effects (2026-07-16): `BattleActionSequence_Tick_Duel` (0x50BDC0, ex-`sub_50BDC0`, cmd
`0xF1`), `BattleActionSequence_Tick_Shot` (0x50BEE0, ex-`sub_50BEE0`, cmd `0xED`/`0xEE`);
`MAG_188_SHOT_Setup_BySequenceMode` (0x5BE370) + `MAG_188_*` globals; the Duel tree
`MAG_274_DUEL` / `_Init` / `_RootTask` / `_MoveTask` / `_Move2..6_Tick`
(0x6897E0 / 0x6898B0 / 0x689990 / 0x689AC0 / 0x68A050, 0x68B2F0, 0x68B700, 0x68B950, 0x68C7B0) and
`MAG274_DUEL_*` globals (`pendingMoveId`, `moveChanged`, `castCtx`, `attackerEntity`, `modelBuffer`,
`moveDurations` 0x110E3E0).

Cast-context pass (2026-07-16): `BattleActionSequence_BuildMagicCastContext` (0x50AFC0,
ex-`sub_50AFC0`), the struct `MagicCastContext` (12 B) + enum `MagicCastFlags`, and the global
`g_MagicCastContext` (0x1D99A78, ex-`RELATED_SLOT_ID_ATTACKER`). Typing that one global absorbed
seven loose globals that were really its fields — `byte_1D99A79`, `word_1D99A7A`,
`RELATED_BATTLE_TASK_68_DATA_ADDR`, `byte_1D99A80`…`byte_1D99A83`. The uniform prototype
`TaskQueueExample *__cdecl f(MagicCastContext *cast_context)` is applied to **all 343 dispatch
entries and all 111 thunk targets**, so every effect init now reads its context symbolically.

Globals: `MAGIC_EFFECT_ACTIVE_FLAG` (0x1D99A64), `MAGIC_EFFECT_INDEX` (0x1D99A68),
`MAGIC_TEXTURE_BUFFER_PTR` (0x1D99A88), `MAGIC_TEXTURE_BUFFER_BASE` (0x20DFAB8),
`MAGIC_ALLOC_COUNT` / `MAGIC_ALLOC_PTRS` (0x21DFABC / 0x21DFAC0),
`MAGIC_EFFECT_TIMEOUT_CTR` (0x1D99A8E, 900-frame failsafe), and the Firaga statics
`MAG143_*` (0x24BECC8–0x24BFB3C block, prim models 0xDDA740/0xDDC578/0xDDCE48, camera track
0xDD9A4C, sound def 0xDDD8F0, `mag142.tim` name 0xDDD8F8).

## Open questions

- Entry layouts of the seven secondary prim-model section types (0x572500…0x573290) —
  the count-prefixed framing is known, per-type entry sizes still to derive.
- Encoding of the `BdPlaySE3D` u32 sound code (bank/index split).
- Identification of effect_ids 226–345 (`MAG_2xx/3xx_UNKNOWN`): which monster attack or
  story cinematic each one is.
- Remaining shifted main-function names in the 34–98 range (fix by walking the table, or
  extend `Fujin/ResearchScript/dump_magic_effects.py` to auto-rename from the `_FL` names).
