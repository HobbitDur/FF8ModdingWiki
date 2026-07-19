---
title: Composite character + weapon animation (runtime)
layout: default
parent: Battle
permalink: /technical-reference/battle/composite-character-weapon-animation/
author: HobbitDur
---

1. TOC
{:toc}

## Overview

A playable character in battle is **two independent battle models** — a body
(`dXcYYY.dat`) and a weapon (`dXwYYY.dat`) — that the engine drives as **one
entity from a single animation clock**. Each file carries its own
[skeleton](../model-sections/skeleton/),
[geometry](../model-sections/model-geometry/) and
[animation pool](../model-sections/model-animation/); the two are never merged
into one skeleton. Instead they are played **in lockstep on a matching animation
index** and drawn one after the other, the weapon positioned relative to the
body's world transform.

This page documents the *runtime* side — how the two models stay in sync and how
the weapon is placed. The file layout (which section holds what) is on
[Character & weapon files](../character-weapon-files/); the *frame timing*
(delta-stream decode, SLOW/FAST half-stepping) is on
[Battle model animation timing](../battle-model-animation-timing/). This page is
the missing middle: the **spatial and structural** composition.

> **Practical upshot for model viewers (Ifrit3D):** to reproduce a character's
> in-game animation you must load **both** files and play the **same-indexed**
> animation on each. The body alone plays with an empty hand; the weapon alone
> plays "floating" the way it does in the character's hand, but neither is
> parented to the other's bones — the two clips are authored to match. See
> [Reproducing it in a viewer](#reproducing-it-in-a-viewer).

## Two anim headers on one entity

Each battle slot (`FF8BattleEntitySlotData`, see
[Battle slot data](../battle-slot-data/)) holds:

- `anim_header` — an inline `BattleAnimHeader` for the **body** (`comFileData` =
  body model, `anim_cmd` = the body's animation state).
- `weaponAnimHeader` — a **pointer** to a separate weapon block (`NULL` for an
  entity with no weapon model). Its `comFileData` is set to the weapon's own
  com-file data by the weapon loader (`Battle_LoadWeaponry`).

`anim_header` starts with a 12-byte `BattleAnimHeader`: `{ uint32 frame_count;
ComFileData* comFileData; ComFileData* comFileDataBis; }`. The weapon block is a
**68-byte** structure that *begins* with the same 12 bytes — which is why the code
declares `weaponAnimHeader` as `BattleAnimHeader*` and reaches the rest by array
indexing (`weaponAnimHeader[1]` = the weapon's `BattleAnimCmd`, `weaponAnimHeader[3]`
= the attach transform). Its true layout (`struct BattleWeaponAnimSlot` in the
IDB):

| Off | Field                | Type               | Meaning                                                              |
|-----|----------------------|--------------------|----------------------------------------------------------------------|
| +0  | `frame_count`        | `uint32`           | (as `BattleAnimHeader`)                                              |
| +4  | `comFileData`        | `ComFileData*`     | Weapon's own skeleton / geometry / animation                        |
| +8  | `comFileDataBis`     | `ComFileData*`     | Double-buffer copy                                                   |
| +12 | `anim_cmd`           | `BattleAnimCmd` ×8 | Weapon animation state (played in lockstep with the body)           |
| +20 | `attach_rotX/Y/Z`    | `int16` ×3         | Attach rotation angles (ZYX); zero in vanilla idle                  |
| +28 | `attach_trans*_src`  | `int16` ×3         | Attach translation source; zero in vanilla idle                     |
| +36 | `attach_transform`   | `Matrix4x3` (32 B) | Weapon base transform, **rebuilt every frame** from the two fields above |

The block is allocated per battle slot at `BD_TASK_LINK_HEADER_SOME.data +
17*slot` (17 dwords = 68 bytes) in `initWeaponAnim` (`0x502670`).

Because the body and weapon each keep their **own** `comFileData` (own skeleton +
own animation pool), advancing "the animation" means advancing *two* separate
delta-stream decodes.

### When there is no weapon model

`initWeaponAnim` sets `weaponAnimHeader = NULL` — i.e. **no second model is drawn**
— for monsters and for **Zell, Edea and Kiros**:

- **Zell** and **Kiros** fight with fists/attached blades: their body already
  contains the "weapon". They still load a **reduced** weapon file
  (`BS_LoadWeaponry_2`) — but only to supply the choreography VM and sounds, not a
  rendered model.
- **Edea** casts: `initWeaponAnim` skips her weapon load entirely
  (`com_id != COM_ID_EDEA`), and her dedicated body loader carries what she needs.
- Every other character loads a normal weapon file **and** gets a
  `BattleWeaponAnimSlot`, so a second model is drawn.

For a viewer this means: Zell/Kiros/Edea are complete from the body file alone;
all other characters need the paired weapon file to look right.

## Lockstep: one index, one clock

### Starting an animation

`Battle_QueueAnimation(entity, animID)` is the only starter for an entity's
skeletal animation. It sets the **same** `animID` on **both** models — weapon
first, then body — via `pre_Battle_ReadAnimation`:

```c
weaponAnimHeader = entity->weaponAnimHeader;
if (weaponAnimHeader)                                  // weapon FIRST
    pre_Battle_ReadAnimation(weaponAnimHeader, &weaponAnimHeader[1], opcode);
return pre_Battle_ReadAnimation(&entity->anim_header, &entity->anim_cmd, opcode);
```

`pre_Battle_ReadAnimation` resets that model's `anim_cmd` (`current_frame = 0`,
`total_frames` = the target animation's frame count, byte/interpolation cursors
cleared), zeroes the skeleton's root position and all per-bone rotation deltas,
then reads frame 0. It does this **identically** for the weapon and the body.

The consequence: **animation index `N` in the body's animation pool is the same
action as index `N` in the weapon's animation pool.** The two clips are authored
as matched pairs — for every body pose that swings the arm, the corresponding
weapon clip moves the weapon so it tracks the hand.

### Advancing each frame

Once per tick, `AnimSeq_UpdateEntityPerFrame` calls
`AdvanceAnimationBy1AndCheckCompletion`, which advances **both** decodes — again
weapon first, then body — with `Battle_ReadAnimation`:

```c
weaponAnimHeader = slot->weaponAnimHeader;
if (weaponAnimHeader)
    Battle_ReadAnimation(weaponAnimHeader, &weaponAnimHeader[1]);   // weapon
return Battle_ReadAnimation(&slot->anim_header, &slot->anim_cmd);   // body
```

There is only one driver per entity, so the two models can never drift: they
start on the same index in the same tick and step together every tick. SLOW/Haste
frame-doubling (see [timing](../battle-model-animation-timing/)) is applied to
both `anim_cmd`s in `Battle_QueueAnimation`, so even the half-step interpolation
stays synchronized. Each model still keeps its **own** `total_frames`, so the two
clips need not be the same length (see the Rinoa note below); completion is
tracked per-model.

### Evidence in the vanilla files

Parsing section 3 (model animation) of every armed character's body and weapon
files confirms the matched-pool design — the body and **all** of that character's
weapons carry the *same number* of animations, in the same order:

| Character | Body anims | Weapon anims (all tiers) | Per-frame counts |
|-----------|:----------:|:------------------------:|------------------|
| Squall    | 42 | 42 | identical |
| Irvine    | 32 | 32 | identical |
| Quistis   | 38 | 38 | identical |
| Rinoa     | 31 | 31 | **2 of 31 differ** (anim 5: 14 vs 15, anim 6: 23 vs 24 — the projectile clips run one frame longer) |
| Selphie   | 33 | 33 | identical |
| Seifer    | 36 | 36 | identical |
| Laguna    | 31 | 31 | identical |
| Ward      | 31 | 31 | identical |

Same tally for the no-weapon-model characters:

- **Zell** (38 body anims) and **Kiros** (34) — their weapon files are the reduced
  5-section form with **no model-animation section at all**: there is simply no
  weapon geometry/animation to play.
- **Edea** (30 body anims) — her body file is a **10-section** self-contained model:
  a normal character body with the weapon's sequence-VM + sounds + bank sections
  spliced in, so no weapon file is loaded for her. See the verified section map in
  [Character & weapon files → Edea](../character-weapon-files/#edea--self-contained-10-section-body).

So for a viewer: match the two pools by index; expect equal counts and (almost
always) equal per-animation frame counts, but don't assume the frame counts are
identical — advance each model by its own length.

## Where "which animation" is decided

Neither model *chooses* its animation — the **animation-sequence VM**
(choreography) does, and that VM lives in the **weapon** file (weapon section 4 =
the monster [Animation sequences](../model-sections/animation-sequences/) block).
At battle start `initAnimationSequenceAtStartBattle` binds the merged per-slot
com-file record so that the entity's `comFileData->comFileAnimSection5` points at
the **weapon's** sequence data; the body file carries no sequence section. The VM
issues `Battle_QueueAnimation` calls (opcodes `< 0x80`, `A0`, idle restart), which
is exactly what fans the chosen index out to both models. This is the concrete
reason a character **must** have a weapon loaded — including the reduced weapon
files of the unarmed fighters (Zell, Kiros).

See [Character & weapon files → the composite bind](../character-weapon-files/)
and [Animation sequences](../model-sections/animation-sequences/) for the VM itself.

## Rendering: body then weapon

`BS_RenderBattleEntity` draws the two models back-to-back into the same frame:

1. Build the entity **world base** matrix = battle camera × entity scale/rotation
   (`ComposeAffineTransform` into a scratch workspace). A back-turned entity gets
   an extra Y rotation so it faces away.
2. `BS_ComputeBonesWorldMatrices(&slot->anim_header, base)` — compose the world
   base onto **every body bone's** local matrix (already posed by this frame's
   `Battle_ReadAnimation`). This leaves the shared `base` matrix untouched.
3. `RenderGeometry(body, …)` — draw the body mesh.
4. If a weapon exists **and** the weapon is not hidden
   (`status_flags & BATTLE_ENTITY_STATUS_FLAG_WEAPON_HIDDEN` clear):
   - `weapon_base = base ∘ weaponAnimHeader[3]` — compose the weapon's attach
     transform onto the **same body world base**.
   - `BS_ComputeBonesWorldMatrices(weaponAnimHeader, weapon_base)` — pose the
     weapon's own bones under that base.
   - `RenderGeometry(weapon, …)` — draw the weapon mesh.

Per-object visibility (`some_flag_data`, the E5 `0x20` / A6 bitmask) is forced to
`-1` (all objects shown) for the weapon pass, so weapon sub-objects are never
subject to the body's part-hiding.

### Placing the weapon

In step 4 the base fed to the weapon is the *body's world base* (camera × scale)
composed with `attach_transform` (`weaponAnimHeader[3]`, at +36 of the weapon
slot). `attach_transform` is **rebuilt every frame** in
`pre_pre_linkedToAnimationSequence`: `ComposeZYXRotationMatrix` turns the three
`attach_rot` angles (+20) into the 3×3 part, and the three `attach_trans_src`
int16 (+28) are sign-extended into the translation part. `initAnimationSequence­
AtStartBattle` **zeroes** all six fields, and no vanilla code writes them for a
normal attack, so `attach_transform` is **identity** — the weapon is posed under
the *plain* entity base.

> **⚠️ Correction (verified against d0c000/d0w000).** An earlier version of this
> page claimed the weapon's own animation clip keys the mesh into the hand under
> that shared base. **That is wrong.** Parsing the files shows the opposite: a
> weapon has a tiny skeleton (Squall's `d0w000` = **2 bones, all geometry bound to
> bone 1**), the animated weapon vertices are centred on the **entity origin** (not
> the hand), and the weapon's per-frame root position ≈ the body's (both ~the
> entity height, no hand offset). With `attach_transform` identity and the weapon
> bones at the origin, the weapon is drawn **at the character's root**, and the
> "held" placement must come from **somewhere still not accounted for here** — most
> likely a per-frame hand-bone transform copied into `attach_trans`/`attach_rot` by
> a path not yet located (the write site is via `weaponAnimHeader[N]` pointer
> arithmetic, so it doesn't show up as a struct-field xref). Until that is found,
> **a viewer cannot reproduce the placement from the weapon clip alone** — it must
> attach the weapon to the body's hand bone explicitly (translate the posed weapon
> to a chosen body bone each frame; the correct bone index is per-character and not
> encoded in the file). See [Reproducing it in a viewer](#reproducing-it-in-a-viewer).

The `attach_rot`/`attach_trans` fields also exist so an effect can rotate or offset
the held weapon (e.g. throwing it) without touching the weapon's skeletal animation.

## Reproducing it in a viewer

For a tool that wants to show a character animating with its weapon (Ifrit3D):

1. **Load both files.** A `dXcYYY` body on its own can only be posed with an empty
   hand; the weapon geometry/animation is in the paired `dXwYYY`.
2. **Play the same animation index on both** skeletons, stepping them together —
   body frame *k* with weapon frame *k*.
3. **Attach the weapon to the body's hand bone.** Contrary to the earlier claim
   above, the weapon clip does **not** self-place into the hand — posed on its own
   it sits at the entity root (blade extending past the head). You must transform
   the posed weapon by a chosen body bone's world matrix each frame (translation to
   the bone is usually enough; the weapon's own clip supplies the blade
   orientation). The correct bone is the weapon-holding hand and is **per-character**
   — it is not stored in the file, so a tool should let the user pick it (or ship a
   per-character lookup once each is confirmed visually).
4. The body's animation pool and the weapon's animation pool have the **same
   count and ordering** of actions; index them in parallel. (The choreography that
   picks indices in-game lives in the weapon's sequence section and is not needed
   just to *play* a given animation.)

Note the body's own [dynamic-texture section](../model-sections/dynamic-texture-data/)
drives eye-blink, and the body's [camera section](../model-sections/camera-sequence/)
holds the per-action camera — neither affects the weapon.

## Reference — key addresses (FF8_EN.exe)

| Address    | Symbol                                 | Role                                                                 |
|------------|----------------------------------------|----------------------------------------------------------------------|
| `0x502670` | `initWeaponAnim`                       | Allocates the 68-B weapon slot (`= NULL` for monsters/Zell/Edea/Kiros); loads body + weapon files |
| `0x5027D0` | `initAnimationSequenceAtStartBattle`   | Binds the composite slot; makes `comFileAnimSection5` = weapon's VM; zeroes the attach fields |
| `0x502AB0` | `pre_pre_linkedToAnimationSequence`    | Per-entity tick task: render + advance; **rebuilds `attach_transform`** from the attach rot/trans fields |
| `0x502D40` | `BS_RenderBattleEntity`                | Draws body then weapon; composes `base ∘ attach_transform`          |
| `0x5095B0` | `BS_ComputeBonesWorldMatrices`         | Composes a world base onto every bone of one skeleton                |
| `0x509520` | `Battle_QueueAnimation`                | Starts an animation index on **weapon then body** (lockstep)         |
| `0x509440` | `pre_Battle_ReadAnimation`             | Resets one model's `anim_cmd`/skeleton for a new index, reads frame 0|
| `0x5094F0` | `AdvanceAnimationBy1AndCheckCompletion`| Per-tick advance of **weapon then body** decode                      |
| `0x508F90` | `Battle_ReadAnimation`                 | Decodes one frame's delta rot/pos into a skeleton, rebuilds geometry |
| `0x508C90` | `ProcessFieldEntitiesTransformation`   | Rebuilds a model's bone world matrices from the posed skeleton       |
| `0x507BF0` | `Battle_LoadWeaponry`                  | Loads the weapon file; sets `weaponAnimHeader->comFileData`          |

The weapon slot layout is captured as `struct BattleWeaponAnimSlot` (68 bytes) in
the IDB, with the attach mechanism and lockstep documented as comments on
`FF8BattleEntitySlotData.weaponAnimHeader` and at the sites above.

## See also

- [Character & weapon files (dXcYYY.dat / dXwYYY.dat)](../character-weapon-files/) — file/section layout.
- [Battle model animation timing](../battle-model-animation-timing/) — delta-stream decode, SLOW/FAST, frame rate.
- [Animation sequences](../model-sections/animation-sequences/) — the choreography VM (in the weapon).
- [Battle slot data](../battle-slot-data/) — `FF8BattleEntitySlotData` fields.
