---
layout: default
parent: Battle
title: "Case study: Firaga animation"
permalink: /technical-reference/battle/firaga-case-study/
---

A complete, line-by-line walkthrough of **one** spell animation — **Firaga** (effect_id 143) —
from the moment the battle engine picks it to the individual particles it draws, and exactly
**what you can change and where**. Firaga is a good reference because it is a plain offensive
spell (no GF cinematic, no summon model): everything it does is representative of how the
~340 in-engine spell effects are built.

Read [Magic Effect Anatomy & Authoring](../magic-effect-anatomy/) first for the general model;
this page is the worked example. All addresses are the **2013 Steam English `FF8_EN.exe`**.
The **Fujin** subtool in FF8UltimateEditor shows the same functions (read-only, decompiled) and
previews the texture.

Firaga is the **director-on-a-frame-timeline** archetype. For the other archetype — a
**state machine** — see the companion [Case study: Cure animation](../cure-case-study/); between
the two you can read essentially every regular spell effect.

1. TOC
{:toc}

## 0. One-paragraph summary

Firaga is **hardcoded C code** compiled into the exe. The only *file* it uses is its texture
`mag142.tim` (in `magic.fs`). When cast, its **init function** allocates two little task
queues, plays a hardcoded camera swoop, uploads the texture, and starts a **director** task.
The director is a 60-frame timeline that, frame by frame, spawns **particle tasks** (sparks, a
central fireball, a burst ring, two flame swirls, ground flames), fires the sound, flashes the
screen, and — on frame 48 — applies the damage. Each particle task draws a **billboard model**
(also hardcoded in the exe) every frame until it dies. When all tasks are gone, the effect ends.

## 1. Getting there: dispatch

```
kernel.bin "Firaga" magic entry, field +0x04 = 143   (the effect_id)
        │  copied into the battle action task (+6)
        ▼
Magic_GetIDLoad(143) @0x50AF20     idx = 143 - 1 = 142
        │
        ├─ MagicList_TextureLoad[142] = 0x61BFC0  MAG_143_FIRAGA_FL   → loads mag142.tim
        └─ MagicList_Logic[142]       = 0x61BFE0  MAG_143_FIRAGA      → the init function
        ▼
BattleActionSequence_Tick_MagicCast @0x50A9A0 (case 4) calls MAG_143_FIRAGA once:
        C3_28_GF_data_pointer = MAG_143_FIRAGA(&attacker_slot)
```

From then on, the single per-frame driver at `0x50093A` ticks `C3_28_GF_data_pointer` (Firaga's
root queue) once per battle frame until it empties. See
[Magic Spell Effect Runtime](../magic-spell-effect-runtime/) for that driver and the 60 fps
implications.

### The texture loader — `MAG_143_FIRAGA_FL` @0x61BFC0

```c
MAG143_timFilePtr = IO_GetFile_MAGIC("mag142.tim");
```

That is the whole loader: read `\FF8\Data\Magic\mag142.tim` from the `magic.fs` archive into a
buffer. `mag142.tim` is a 640×256 8-bpp TIM **texture atlas** — the flame/spark sprites the
billboards sample from.

## 2. The Firaga data block (`.data`)

Everything that isn't code lives in two clusters of globals. **These are what a data editor
patches.**

### Runtime scratch (`0x24BE…/0x24BF…`) — written at cast time, don't edit statically

| Symbol | Address | Meaning |
|---|---|---|
| `MAG143_castContextPtr` | 0x24BFB10 | pointer to the action context (attacker, flags, target list) |
| `MAG143_attackerSlot` | 0x24BFB14 | attacker battle-slot id |
| `MAG143_timFilePtr` | 0x24BFB18 | loaded `mag142.tim` buffer |
| `MAG143_targetEffectPos` | 0x24BFB20 | per-target world position (x,z) filled on frame 0 |
| `dword_24BFB24` | 0x24BFB24 | per-target world position (y) + "active" flag |
| `MAG143_primBufferBase/Cursor` | 0x24BFB38 / 0x24BFB3C | double-buffered GPU packet write cursor |
| `MAG143_effectQueues` | 0x24BECE0 | the two BdLink task queues (root + effect) |

### Static assets (`0xDD…`) — **the moddable Tier-2 data**

| Symbol | Address | What it is | Consumed by |
|---|---|---|---|
| `aMag142Tim` | 0xDDD8F8 | the string `"mag142.tim"` | the loader |
| `MAG143_cameraAnimData` | 0xDD9A4C | keyframed **camera track** (the strike swoop) | `Battle_PlayCameraAnimation` |
| `MAG143_soundDef` | 0xDDD8F0 | **sound** id `0x00049418` | `BdPlaySE3D` |
| `MAG143_primModel_Spark` | 0xDDCE48 | billboard **model** for the sparks | `Effect_RenderPrimModel` |
| `MAG143_primModel_TargetFireball` | 0xDDC578 | billboard model for the central fireball | `Effect_RenderPrimModel` |
| `MAG143_primModel_FlameSwirl` | 0xDDA740 | billboard model for the swirls | `Effect_RenderPrimModel` |
| `unk_DDD208` | 0xDDD208 | model for the burst ring | `Effect_RenderPrimModel` |
| `unk_DDA594` | 0xDDA594 | **sequence** for the ground flames | `InitEffectSequenceFromData` |

Prim-model and camera-track binary layouts are documented in
[Magic Effect Anatomy & Authoring](../magic-effect-anatomy/#tier-2-data-formats).

## 3. The task tree

`MAG_143_FIRAGA` (@0x61BFE0) builds this and returns the **root queue**:

```
root queue  (1 node)   ── MAG_143_FIRAGA_RootTask_RunEffectQueue @0x61CDA0
effect queue (≤100)    ── MAG_143_FIRAGA_Director_Tick          @0x61C0A0
                            └── spawns, over its 60 frames, into the effect queue:
                                MAG_143_FIRAGA_SparkParticle_Tick   @0x61CBB0
                                MAG_143_FIRAGA_TargetFireball_Tick  @0x61CB10
                                MAG_143_FIRAGA_Burst_Tick           @0x61C870
                                MAG_143_FIRAGA_FlameSwirl_Tick      @0x61C9C0
                                MAG_143_FIRAGA_AreaFlame_Tick       @0x61C6B0
```

- **Init** — saves the cast context, `BdLink_InitTaskQueuePool` on the root queue (1×0x10-byte
  node) and the effect queue (100×0x24-byte nodes), adds the root task and the director. Unless
  the "no camera" flag (context +1 bit 0) is set, it plays `MAG143_cameraAnimData` and queues
  the `mag142.tim` VRAM upload. Returns `&MAG143_effectQueues`.
- **Root task** (`…RootTask_RunEffectQueue`) — runs every frame: flips the double-buffered GPU
  packet cursor (`primBufferBase` / `+0x10000` on alternate frames), then
  `ExecuteTaskQueue(effect queue)`. It self-destructs (returns 2) only when the effect queue is
  empty — i.e. when the whole animation is over.

## 4. The director timeline — `MAG_143_FIRAGA_Director_Tick` @0x61C0A0

One node; the word at `node[1].flags_and_priority` is a **frame counter** that runs 0 → 60.
Each tick it reads the counter and acts:

| Frame(s) | What happens | Code / data touched |
|---|---|---|
| 0 | capture the target's effect position (midpoint of bones 0xF0/0xF1) | `GetDefaultEffectPosition` → `MAG143_targetEffectPos` |
| 1 | play the cast sound | `BdPlaySE3D(MAG143_soundDef, …)` |
| 1–14 | spawn **`frame/6 + 1` spark particles** per frame, each with a random unit-sphere velocity | `MAG_143_FIRAGA_SparkParticle_Tick`; `rand`, `NormalizeVectorToFixedPoint`, `FixedPointCrossProduct` |
| 4 | spawn the **central fireball** (grows every frame) | `MAG_143_FIRAGA_TargetFireball_Tick` |
| 32 | begin the full-screen **flash** | `au_re_BdLinkTask_6(0,1,2,255)` |
| 33 | spawn the **burst ring** + **two flame swirls** (one rising, one sinking, random spin) | `MAG_143_FIRAGA_Burst_Tick`, `MAG_143_FIRAGA_FlameSwirl_Tick` ×2 |
| 36–48 | spawn **3 ground flames per frame** around the target, spread by `rand`, clamped near the shadow/ground height | `MAG_143_FIRAGA_AreaFlame_Tick` |
| 44 | if the action has more targets, chain a **new director** for the next target | `AddTaskToQueue(… Director_Tick)` |
| 48 | **apply the result** — damage number + HP change | `ApplyActionResultToTarget` |
| 52–60 | **fade the flash out** (`(60 − frame) << 8`) | `Effect_SetScreenFlash` |
| > 60 | director returns 2 → dies; last-target run clears the flash | |

Two things worth stressing:

- **Damage timing is just a frame number** (48). The visual and the mechanical hit are only
  coupled by this constant. Move it and the numbers pop earlier/later.
- **Multi-target** is a self-chaining director (frame 44), one per target, each reading its own
  `sequence_id` into the shared position arrays.

## 5. The particle tasks

All five follow the same shape: build a transform, allocate an 88- (or 180-)byte render header,
point it at a prim model, set blend/tint, hand it to the renderer, free the header, then advance
their own state and return 2 when their life expires. What differs is the **model**, the
**motion**, the **blend flags**, and the **lifetime**.

| Task | Model | Motion | Blend (+28) | Life | Notes |
|---|---|---|---|---|---|
| `SparkParticle_Tick` @0x61CBB0 | `primModel_Spark` | fly along stored random velocity, camera-aligned via axis-angle | 48 → 240 | 20 f | colour ramps with frame (`4096−682·f`, then `682·(f−14)`) |
| `TargetFireball_Tick` @0x61CB10 | `primModel_TargetFireball` | accelerating growth (rate `+= rate>>6` each frame) | 48 | until f33 | lives f4→33, dies when the director clears the target's active flag; `TransformCameraByShadowRotation` billboards it upright |
| `Burst_Tick` @0x61C870 | `unk_DDD208` | expands (`next -= next/12`), spun by ZYX matrix | 51 → 243 | 20 f | fades in after frame 10 (`409·(f−10)`) |
| `FlameSwirl_Tick` @0x61C9C0 | `primModel_FlameSwirl` | rises or sinks (signed step) with a random spin | — | 24 f | two are spawned, opposite vertical drift |
| `AreaFlame_Tick` @0x61C6B0 | `unk_DDA594` (a **sequence**) | rises from the ground, darkens with height (`160·h/2000 − 96`) | 12 | 16 f | uses `InitEffectSequenceFromData`, not a single model; has a start delay via `sequence_id` |

The recurring helper calls — `BuildAxisAngleRotationMatrix`, `scale3DMatrix`,
`ComposeAffineTransform`, `Field_readCamRotationScale`, `Effect_RenderPrimModel`,
`Field_Alloc`/`Field_Free` — are the shared "effect SDK" listed in
[Magic Effect Anatomy & Authoring](../magic-effect-anatomy/#shared-helper-library-the-effect-sdk-inside-the-exe).

### Render header fields (built per draw by each task)

`Field_Alloc(88)` then:

| Offset | Meaning (from the Firaga tasks) |
|---|---|
| +0 | pointer to the prim model (e.g. `&MAG143_primModel_Spark`) |
| +8/+9/+10 | RGB tint bytes |
| +12 | colour / alpha parameter (the ramps above) |
| +28 | blend-mode flags (48 = additive-ish, 240/243 = modulate; observed values) |

## 6. How to modify Firaga

Three tiers, cheapest first. Tiers 1–2 need no code; see the roadmap in
[Magic Effect Anatomy & Authoring](../magic-effect-anatomy/#creating-a-new-spell-animation-wind-maker--tool-roadmap).

### Tier 1 — reskin (no exe edit)

- **Recolour / redraw the flames:** edit `mag142.tim` (the 640×256 atlas) and repack `magic.fs`
  (or use a direct-file loader like FFNx). Every billboard samples this one texture, so this
  restyles the whole spell. Fujin's **Texture** tab previews and extracts/replaces it.
- **Give another spell Firaga's animation:** set that spell's kernel magic entry **+0x04** to
  143 (via SolomonRing/Doomtrain). It will now play the Firaga effect regardless of its own
  element/power.

### Tier 2 — data patching (hex-edit `.data`, no code)

All of these are byte edits to the static assets in section 2, no recompilation:

- **Retime the spell** — patch the frame constants inside `MAG_143_FIRAGA_Director_Tick`
  (they are compare-immediates in the code, not `.data`, but still in-place byte patches):

  | Constant | Meaning | Code address |
  |---|---|---|
  | 1..14 | spark spawn window | 0x61C0FB–0x61C10F |
  | 4 | fireball spawn frame | 0x61C2B2 |
  | 32 | flash-begin frame | 0x61C2F8 |
  | 33 | burst + swirl frame | 0x61C314 / 0x61C402 |
  | 36..48 | ground-flame window | 0x61C451 |
  | 48 | **damage frame** | 0x61C574 |
  | 60 | director lifetime | 0x61C679 |

- **Change the sound:** patch the u32 sound id at `MAG143_soundDef` (0xDDD8F0).
- **Change the camera:** replace the track at `MAG143_cameraAnimData` (0xDD9A4C) — same format
  as battle-stage camera data, so the `.X`/camera-sequence tooling applies.
- **Change the shapes/UVs:** edit the prim models (`0xDDA740`, `0xDDC578`, `0xDDCE48`,
  `0xDDD208`) — vertex/UV/section data in the format under
  [Tier-2 data formats](../magic-effect-anatomy/#tier-2-data-formats).
- **Change particle counts / lifetimes / colour ramps:** the immediates in each `_Tick`
  (e.g. spark life `20` at 0x61CD8D; the `/6 + 1` spark-count divisor at 0x61C124).

### Tier 3 — new behaviour (code / DLL)

To do something the existing tasks can't (new motion, new emitter logic, more particle types),
you write code. On the 2013 exe that means an **FFNx** build (Hext can't host new code there):
add tasks that call the same shared helpers by address, draw your own prim models, and register
the whole thing either in place of Firaga's init or in a **free effect slot** (224, 225, or
346–400) that a new spell's kernel +0x04 points to. The generic, data-driven-director approach
(a timeline file + a texture, interpreted by one DLL routine) is described in the anatomy page.

## 7. Recipe: add a brand-new spell animation

Say you want a new spell, **"Wind Maker"**, with its own effect. You do **not** overwrite an
existing spell — you claim one of the **free effect slots** (224, 225, or 346–400: both table
pointers are `0` there) and fill it in. Two levels of effort.

### The two table writes (common to both recipes)

The dispatch is just two parallel pointer arrays, indexed by `effect_id − 1`:

```
MagicList_Logic        @ 0xC81774   → MagicList_Logic[N-1]        = your init function
MagicList_TextureLoad  @ 0xC81DB8   → MagicList_TextureLoad[N-1]  = your texture loader
```

For a free slot **N**, the two dwords to write live at:

```
0xC81774 + 4*(N-1)     ← init function address
0xC81DB8 + 4*(N-1)     ← texture-loader address (may be 0 if the effect loads no file)
```

Then point a spell at it: set that spell's **kernel magic entry field +0x04** to **N**
(SolomonRing / Doomtrain). Now casting the spell runs your effect.

> Free slots have `0` in both arrays, so writing them displaces nothing. Pick e.g. **224**.

### Recipe A — reuse an existing animation with your own texture (no new logic)

The cheapest real "new spell": your effect plays Firaga's animation but samples **your** atlas.

1. **Add a tiny texture loader.** Firaga's is literally
   `push "mag142.tim"; call IO_GetFile_MAGIC; mov MAG143_timFilePtr, eax; ret`. Write the same
   ~20 bytes but with your file name (`"windmaker.tim"`) — in a code cave or, cleanly, in an
   FFNx DLL. Drop `windmaker.tim` into `magic.fs` (any name works; the loader reads whatever
   string you give it).
2. **Wire the table:** `MagicList_Logic[223] = 0x61BFE0` (reuse `MAG_143_FIRAGA`),
   `MagicList_TextureLoad[223] =` your loader from step 1.
3. **Point a spell:** kernel magic entry +0x04 = 224.

Caveat: reusing `MAG_143_FIRAGA` means you also reuse its **static globals** (`MAG143_*`) — fine
because only one magic effect is active at a time in battle. The result is a **recoloured
Firaga on a new effect_id**. Swapping which init you reuse (Blizzard, Tornado, Thundara…) picks
a different motion. This is the tier a data-only tool (Fujin) can drive end-to-end.

### Recipe B — a genuinely new animation (FFNx DLL)

To get new *behaviour* (new emitters, timing, motion), you supply code. On the 2013 exe that
means an **FFNx** build (`AF3DN.P`) — Hext can't host new code, and packed `.text` has no room.
Mirror Firaga's structure:

1. **Assets.** Author `windmaker.tim` (the texture atlas) for `magic.fs`, and prepare your
   **prim models** (billboard geometry, same section format as `MAG143_primModel_*` — see
   [Tier-2 data formats](../magic-effect-anatomy/#tier-2-data-formats)). Models can live in your
   DLL's own memory; `Effect_RenderPrimModel` only needs a pointer. Pick a **camera track** to
   reuse (any existing spell's, e.g. `MAG143_cameraAnimData`) or author one.
2. **Static state.** Reserve your own globals in the DLL: two BdLink queues (a 1-node root and
   an N-node effect queue), a GPU-packet double-buffer, per-target position array — the
   `MAG143_*` block is the template for what you need.
3. **Loader `WindMaker_FL`.** `your_tim = IO_GetFile_MAGIC("windmaker.tim");`
4. **Init `WindMaker_Init(cast_context)`.** Copy Firaga's `MAG_143_FIRAGA` almost verbatim:
   - save `cast_context`,
   - `BdLink_InitTaskQueuePool` on your root + effect queues,
   - `AddTaskToQueue(root, WindMaker_RootTask)` and `AddTaskToQueue(effect, WindMaker_Director)`,
   - unless the no-camera flag: `Battle_PlayCameraAnimation(&your_or_reused_camera)` and
     `Battle_QueueTIMUpload_GetEOF(your_tim)`,
   - `return &your_root_queue;` (becomes `C3_28_GF_data_pointer`).
5. **Root task `WindMaker_RootTask`.** Flip the GPU double-buffer, `ExecuteTaskQueue(effect
   queue)`, return 2 when it empties. (Firaga's `…RootTask_RunEffectQueue` verbatim.)
6. **Director `WindMaker_Director`.** Your timeline. Use a frame counter in the node payload;
   at chosen frames `AddTaskToQueue(effect queue, WindMaker_Particle_Tick)`, spawn positions
   from `GetDefaultEffectPosition`, play sound with `BdPlaySE3D`, flash with
   `Effect_SetScreenFlash`, and — critically — call **`ApplyActionResultToTarget` on your "hit"
   frame** so damage lands. Handle multi-target by chaining a new director (Firaga frame 44).
7. **Particle ticks `WindMaker_*_Tick`.** For each: build a transform
   (`BuildAxisAngleRotationMatrix` / `scale3DMatrix` / `ComposeAffineTransform`),
   `Field_Alloc(88)` a render header, set +0 = your model, +8/9/10 tint, +12 colour, +28 blend,
   `Effect_RenderPrimModel(...)`, `Field_Free(88)`, advance, return 2 at end of life.
8. **Register** (from the DLL, at load): write `MagicList_Logic[223] = &WindMaker_Init` and
   `MagicList_TextureLoad[223] = &WindMaker_FL`.
9. **Point a spell:** kernel magic entry +0x04 = 224.

All the helper addresses you need are in the [function reference](#8-function--symbol-reference-firaga)
below; call them by address from the DLL.

**The high-leverage design.** Instead of hand-writing a director + ticks per spell, implement
**one generic, data-driven director** in the DLL that reads a small mod file — a timeline of
`{frame, action, params}` records plus emitter descriptions — and drives the standard helpers
from it. Then "add a new spell" becomes *write a timeline file + a texture*, no compiler, and a
tool can generate both. This is the intended end state for the Fujin authoring workflow.

### Checklist

- [ ] `windmaker.tim` in `magic.fs` (+ prim models if Recipe B)
- [ ] loader + (Recipe B) init/director/tick code in the FFNx DLL
- [ ] `MagicList_Logic[N-1]` and `MagicList_TextureLoad[N-1]` written at load
- [ ] a spell's kernel entry **+0x04 = N**
- [ ] verify in-game: animation plays, **damage lands on the hit frame**, effect ends cleanly

## 8. Function & symbol reference (Firaga)

| Address | Name | Role |
|---|---|---|
| 0x61BFC0 | `MAG_143_FIRAGA_FL` | texture loader (`mag142.tim`) |
| 0x61BFE0 | `MAG_143_FIRAGA` | init: build queues, camera, upload, start director |
| 0x61CDA0 | `MAG_143_FIRAGA_RootTask_RunEffectQueue` | per-frame: flip GPU buffer, run effect queue |
| 0x61C0A0 | `MAG_143_FIRAGA_Director_Tick` | the 60-frame timeline |
| 0x61CBB0 | `MAG_143_FIRAGA_SparkParticle_Tick` | spark billboard |
| 0x61CB10 | `MAG_143_FIRAGA_TargetFireball_Tick` | growing central fireball |
| 0x61C870 | `MAG_143_FIRAGA_Burst_Tick` | expanding burst ring |
| 0x61C9C0 | `MAG_143_FIRAGA_FlameSwirl_Tick` | rising/sinking flame swirl |
| 0x61C6B0 | `MAG_143_FIRAGA_AreaFlame_Tick` | ground flames (sequence-based) |

Shared helpers used: `BdLink_InitTaskQueuePool` (0x508300), `AddTaskToQueue` (0x508360),
`ExecuteTaskQueue` (0x508420), `Battle_PlayCameraAnimation` (0x5099A0),
`Battle_QueueTIMUpload_GetEOF` (0x505E30), `GetDefaultEffectPosition` (0x571400),
`Effect_RenderPrimModel` (0x572200), `InitEffectSequenceFromData` (0x571C80),
`BuildAxisAngleRotationMatrix` (0x5714F0), `Effect_SetScreenFlash` (0x5713E0),
`BdPlaySE3D` (0x5013A0), `ApplyActionResultToTarget` (0x506690),
`Field_Alloc`/`Field_Free` (0x5082B0/0x5082D0).
