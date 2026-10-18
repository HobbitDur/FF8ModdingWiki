---
layout: default
parent: Battle
title: Battle Cameras
permalink: /technical-reference/battle/battle-cameras/
---

Battle action cameras have two separate sources: an optional opening shot from the acting
entity's camera collection, followed by camera work started by the visual effect. A monster's
animation-sequence ID, magic ID, visual-effect ID, camera-animation index, and camera category
are different values.

This page follows the monster action path, starting with ordinary Magic, and compares the
other command branches. It complements the [camera format and script reference](../model-sections/camera-sequence/).

The code was checked in the 2013 Steam English `FF8_EN.exe` database (MD5
`be8b278becf6757bb811acd45d717d9c`). Addresses and analysis names below refer to that build.
The struct member names are reverse-engineering annotations, not recovered source symbols.
The general path is established by static analysis; the exact shot for an individual effect
requires following that effect's code and camera script.

1. TOC
{:toc}

## The path from an ability to a camera

```text
Monster AI chooses an ability slot
    |
    +-- Section 7 ability entry: command type, actor sequence ID, ability ID
            |
            +-- Actor sequence ID -> section 5 actor animation sequence
            |       |
            |       +-- Optional opening shot -> actor's section 6 camera collection
            |
            +-- Ability ID -> command-specific kernel record -> visual-effect ID
                    |
                    +-- Effect initializer -> camera script and/or camera code
                            |
                            +-- Camera keyframes / calculated camera movement
                                    |
                                    +-- Effect/script cleanup and possible return to saved view
```

The opening shot and the effect camera can both play during one action. Suppressing the
opening shot does not imply that the visual effect's camera is suppressed.

## Where the action values come from

The monster AI is in [DAT section 8](../model-sections/battle-scripts-ai/).
Its normal **USE** instruction chooses an ability slot from the active level-tier list in
[section 7, information and stats](../model-sections/information-stats/#abilities).

Each ability entry is four bytes:

| Entry offset | Size | IDA field | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | `typeID` | Command type: e.g. Magic `2`, Item `4`, Monster Attack `8` |
| `+0x01` | `u8` | `animscript` | Actor animation-sequence ID |
| `+0x02` | `u16` | `id` | Ability ID interpreted according to the command type |

The three lists each contain 16 entries:

| Level-tier list | Offset relative to section 7 |
|---|---|
| Low | `0x34` |
| Medium | `0x74` |
| High | `0xB4` |

For the normal USE path, the selected entry's section-relative address is:

```text
0x34 + levelTier * 0x40 + abilitySlot * 4
```

Here `levelTier` is 0, 1, or 2. `MonsterAI` reads the command type at `0x489823`,
ability ID at `0x489827`, and sequence ID at `0x48982C`, then passes them to
`computeCommandAction`. Prepared-action AI instructions can supply/override the action
values; the ability-table route is not the only AI route.

For command `2`, `id` indexes `K_MAGIC`, whose `specialActionID` supplies the visual-effect
ID. For command `8`, `id` indexes `K_ENEMY_ATTACK`, whose `attackAnimation` supplies the
effect ID and whose `cameraChange` supplies the opening-camera selector.

Neither the ability's actor sequence ID nor its ability ID is itself a camera-animation index.

## The queued action record

`computeCommandAction` writes these resolved values into `BattleActionTaskData`.
The record size and array stride are `0x14` (20 bytes); this is runtime data, not the
four-byte ability entry stored in the DAT.

| Offset | Size | Member | Meaning / previous IDA name |
|---|---|---|---|
| `+0x00` | `u8` | `slotIdAttacker` | Attacking entity slot |
| `+0x01` | `u8` | `commandType` | `CommandType` |
| `+0x02` | `u8` | `animationSequenceId` | Actor sequence to request; formerly `unk3` |
| `+0x03` | `u8` | `cameraChange` | Enemy-attack opening-camera selector; formerly `unk4` |
| `+0x04` | `u16` | `abilityId` | Command-dependent ID or internal sentinel; formerly `word_1D280C8` |
| `+0x06` | `u16` | `effectId` | Visual-effect ID; formerly `unk6` plus the incorrectly separate `slotId` byte |
| `+0x08` | pointer | `targetData` | Per-target result records |
| `+0x0C` | pointer-sized | `attackSequenceResultArray` | Existing IDA name; the command builder stores the action-name text pointer here, later used by `AnimSeqBB_handleText` |
| `+0x10` | `u8` | `target_count` | Number of targets for this action |
| `+0x11` | `u8` | `actionCountMinus1` | Action-chain count minus one, used from the first record |
| `+0x12` | `u8` | `dword_1D280D8_03` | Unknown; likely tail alignment padding |
| `+0x13` | `u8` | `dword_1D280D8_04` | Unknown; likely tail alignment padding |

Bytes `+0x06` and `+0x07` form **one 16-bit effect ID**. The high byte is not a target
slot. `abilityId` and `effectId` must also remain distinct: the former selects a
command-specific kernel record; the latter selects the visual effect.

For the final two bytes, no semantic read/write was identified in the reviewed action
producers and consumers (`computeCommandAction`, `BattleAction_ExecuteCommand`, and
`BattleTask68_LoadActionContext`). Their position after two byte-sized counts is consistent
with padding to a four-byte boundary. This is an inference, not an exhaustive proof across
every effect implementation. Preserve both bytes and the 20-byte stride.

## Ordinary monster Magic: the optional opening shot

### Which action path runs

`BattleTask68_DispatchActionSequence` chooses the presentation handler. On its generic path:

| Condition, in order | Handler / consequence |
|---|---|
| `abilityId == 0xFFFF` | Separate no-target/sentinel handler |
| `effectId != 0` and `animationSequenceId != 0` | Cast path: actor sequence, optional opening camera, then effect |
| `effectId != 0` and `animationSequenceId == 0` | Direct-effect path; no opening-camera selection here |
| `effectId == 0` | Actor-action path that can still request an opening camera |

There are additional command-specific handlers, so this table is not a replacement for the
whole dispatcher switch.

On the normal cast path, `BattleActionSequence_Tick_MagicCast` requests the actor sequence
at `0x50AA6C`, calls `cameraWhenDoingAction` at `0x50AA7E`, loads the effect, waits for the
opening camera and actor cues, then invokes the effect initializer at `0x50AC25`.

### Whether an opening shot is enabled

Before choosing an index, `sub_505F00` decides whether to request an opening camera.

For ordinary Magic it requires an enabled internal camera-control state and a non-null
actor camera collection. Its frequency calculation (`au_re_BS_GetRandomCamera_Probably`)
uses an actor accumulator, random values, and an index initialized from
`4 - SG_SETTING.cameraMovement`. There are also encounter/model exclusions.
The internal state can alter this gating, so the Camera Movement option is not the sole input.

The Magic/Draw/shared-command branch in `cameraWhenDoingAction` also suppresses its shot
when `BattleUI_GetTargetDisplayMode() == 1`. This is an on-model targeting UI state,
not an actor sequence number or a camera index.

These checks concern the opening shot. The effect-camera path has its own flags and code.

### The hardcoded monster choice: camera 0 or 1

After the gates, the monster branch (`com_id >= 0x10`) selects:

```cpp
// Simplified equivalent of the selection around 0x506283:
if (actor.state->basedAnimSeq == 1 && action.animationSequenceId == 11)
    cameraIndex = 0;
else
    cameraIndex = 1;

BS_GetCameraAnimationPointer(actor.command_queue->camera_animation_collection,
                             cameraIndex);
```

Both camera numbers are **zero-based entries in the acting monster's own section 6**,
not entries in the battle stage's camera collection. `battle_monster_dat_loader` binds
that collection to the actor at load time.

The two values in the condition have different roles:

| Value | Meaning |
|---|---|
| `action.animationSequenceId` | The actor sequence requested for this action, normally from the ability's `animscript` |
| `actor.state->basedAnimSeq` | Saved base/return sequence in the actor's runtime state |
| `actor.state->currentAnimSeqId` | Sequence currently executing; **not** the field tested against 1 |

Initialization normally sets the base sequence to 1, with status/spawner-dependent
alternatives. Opcode `A3` can adopt the executing sequence as the base; `E5 0x0B` can
also change it. Starting an action through `someResetBattleStateEntity` updates
`currentAnimSeqId` without replacing `basedAnimSeq`.

Thus an actor can be executing sequence 11 while its saved base is still 1:

| Saved base | Action sequence | Opening-camera index |
|---|---|---|
| 1 | 11 | 0 |
| Not 1 | 11 | 1 |
| 1 | Not 11 | 1 |
| Not 1 | Not 11 | 1 |

This selection is deterministic. Changing the spell's magic ID alone does not change it.

An entry can be empty: if its first control word is `0xFFFF`, the camera player ends
immediately without reading keyframes. Selecting camera 1 does not guarantee a second
visible shot.

The monster branch separately stores `CURRENT_CAMERA_ANIMATION[0] = 8`. That is context
available to the effect's camera script through `C3 00`; it is **not** the 0/1 index
passed to the actor-collection player.

## Which command types share the rule?

The `animationSequenceId` field is shared across commands. The camera rule is only one
branch of `cameraWhenDoingAction`; the command type is checked **before** the sequence
condition.

Command IDs below are decimal unless prefixed with `0x`.

| Command types | Opening-camera selection in this function |
|---|---|
| 2 Magic; 6 Draw; 24 Mad Rush; 25 Treatment; 26 Recover; 27 Revive; 29 Card; 30 Doom; 32 Absorb; 33 LV Down; 34 LV Up | Shared branch: monster actors use the base/sequence condition above; character actors have a separate randomized 0-5 selection |
| 4 Item | No opening-camera case here; an item visual effect can still perform camera work |
| 8 Monster Attack | Uses `action.cameraChange`, not the sequence-11 condition |
| 5, 11, 14, 15, 17, 18, 19, 20, 21, 22, 31, `0xEF` | Random actor-collection entry 6 or 7 |
| 16 Slot | Random actor-collection entry 6 or 7, with separate script-context handling |
| `0xF4`, `0xFE` | History/random-based actor-collection choice among 0-5 |
| Other values | No matching selection case in this function |

These are branches present in the function, not a claim that every command is reachable by
a vanilla monster. The appropriate action handler and earlier gates must still reach this
function with the opening-shot request enabled. Draw additionally skips this shot for
`effectId == 15`.

For character actors in the shared branch, the candidate is
`((PRNG & 3) + actorHistory + 2) % 6`. Multiple affected targets, or particular character
target animation statuses (`0x41021`), clear its low bit before the history is stored.
This randomized character path must not be applied to monster Magic.

### Enemy attack cameraChange

For command 8, `computeCommandAction` copies byte `+0x04` of the
[enemy attack kernel record]({{site.baseurl}}/technical-reference/main/kernel/enemy-attacks/#section-structure)
into `action.cameraChange`.

| Value | Opening-camera request |
|---|---|
| `0xFF` | Disabled by the earlier request gate; not camera index 127 |
| `0x00-0x7F` | Requested index, subject to the probability and target-display checks |
| `0x80-0xFE` | Requested index `value & 0x7F`; forced branch bypasses those probability/UI checks |

The forced branch still requires the earlier internal camera-control/collection gate.
The index is resolved against the **actor's own collection**, so the same kernel byte can
produce different shots for different actors. An actor sequence of 12, for example, does
not imply camera 1 when the command is 8: this command takes a different switch branch.

## The spell or attack effect can start another camera

`Magic_GetIDLoad(effectId)` resolves the visual-effect implementation through
`MagicList_Logic[effectId - 1]`. The magic ID and effect ID are different number spaces.

The effect initializer receives `MagicCastContext`, including the actor and action data.
It can call `Battle_PlayCameraAnimation(cameraData)`, spawn camera tasks, or calculate
camera motion directly. Follow the particular implementation; there is no universal
promise that every effect starts the same kind of camera.

For example, the ordinary Fire initializer at `0x6298A0` calls
`Battle_PlayCameraAnimation(&MAG002_FIRE_cameraAnim)` at `0x629975` when
`(castContext->flags & 1) == 0`. The full camera block is at `0xDED5FC`.
This demonstrates the effect-camera path independently of any particular monster.

The simplified/reflected cast handler sets context flag bit 0. Effects such as Fire use
that bit to skip their camera-start/TIM-upload block. It is separate from the opening-shot
probability decision.

### What is a camera data block or blob?

**Blob** is programming shorthand for a block of binary data, not a separate FF8 file
extension or a camera mode. A full camera data block has this header:

| Block offset | Type | Meaning |
|---|---|---|
| `+0x00` | `u16` | Pointer count |
| `+0x02` | `u16` | Relative byte offset to the camera-setting script |
| `+0x04` | `u16` | Relative byte offset to the camera-animation collection |
| `+0x06` | `u16` | Size field |

Both relative offsets are measured from the start of the block. Do not assume fixed
script/collection lengths from a decompiler's inline struct layout.

```text
Full camera data block
    Header
    Camera-setting script: chooses shots and their timing
    Camera-animation collection: keyframes defining those shots
```

`Battle_PlayCameraAnimation` calls `BS_GetCameraHeaderPointers`, installing the script and
collection pointers. `BS_UpdateCameraSequence` runs the script. Opcode `00 XX` plays index
XX; opcode `05 XX` obtains the index through the camera special-variable reader.

Monster DAT section 6 is different: it contains **only a bare animation collection**,
without that full header or a camera-setting script. Actor section 5 contains actor
animation-sequence instructions; it does not contain section-6 camera keyframes.

## How an index becomes camera movement

`BS_GetCameraAnimationPointer(collection, index)` decodes:

```cpp
set  = (index >> 4) & 0xF;
slot = index & 7;
```

Bit 3 is ignored by this decoder. Each set contains eight signed 16-bit animation
pointers, multiplied by two and resolved relative to the set start. Set pointers in the
collection header are byte offsets relative to the collection start. A null collection
or out-of-range set starts no camera task.

`BS_Camera_ReadAnimation` reads the selected animation's blocks and keyframes.
`ProcessCameraAnimation` interpolates position, look-at point, projection/FOV parameter,
and roll. Coordinate modes can place these values in world space or relative to actor,
target, bones, and other battle reference frames. The same keyframes can therefore
produce different world-space positions for different actors.

`updateBattleCamera` runs the camera script and task queue, applies the active camera
or return-view blend, and exposes the render-facing position/look-at values.
`BS_Camera_BuildViewMatrixApplyShake` builds the view matrix and applies shake offsets.

## Camera category is a separate input

Section 7 byte `0xF6` (246), `camera_category`, is converted to the entity's
`cameraDataRelated` value at initialization:

```cpp
if (category & 8)
    cameraDataRelated = 5;
else if (category & 4)
    cameraDataRelated = 4;
else
    cameraDataRelated = 3 - category;
```

Camera scripts read the **target's** runtime value with `C3 15`, and can branch on it
to select framing. Actor sequences can change their runtime value with `E5 2B`.
Scripts can also read the attacker, target, affected-target count, animation status,
and random values.

This category does not directly choose the caster's opening camera 0/1. Its effect
depends on whether the camera script reads it and how the script uses it.
See [Camera category](../model-sections/information-stats/#byte-246-camera-category).

## Camera cleanup and return

The engine saves a return pose through `BS_Camera_CaptureReturnView`. When an effect ends,
`Magic_EffectEnd_ResetCameraAndEntityFlags` requests a return if the internal camera mode
is not 3 and either `g_BattleCam_ScriptShotActive` is nonzero or `CAMERA_FLAG_RELATED & 0x8000`
is set. It clears the active marker and sets `Battle_Camera_ReturnViewBlend = 4096`.

`updateBattleCamera` snaps to the saved pose when that blend value is at least 4096;
intermediate nonzero values blend toward it. The cleanup is conditional: do not assume
that merely ending an effect always restores the view. Effects can explicitly arm the
return with `BS_Camera_ArmReturnAfterEffect`.

## How to trace or modify an action

1. Find the AI instruction selecting the action, and its active level-tier ability entry.
2. Record the command type, actor sequence ID, and ability ID separately.
3. Follow `computeCommandAction` to obtain `effectId` and any `cameraChange`.
4. Check which presentation handler the dispatcher selects and whether it requests an opening shot.
5. For monster Magic in the shared branch, inspect the saved base sequence and the requested
   sequence; resolve index 0/1 in that monster's section 6.
6. For command 8, resolve the kernel camera selector in the actor's collection instead.
7. Follow `MagicList_Logic[effectId - 1]` into the effect initializer. Find its camera-start
   calls or procedural camera code, then follow the script's actual branches.
8. Check coordinate modes, target category, camera flags, and cleanup for the observed cast.

| Desired change | Data/code to inspect |
|---|---|
| Opening casting shot | Monster section 6 and the hardcoded selection/gates |
| Which actor sequence performs the action | Ability `animscript`, section 5, or prepared AI action |
| Opening shot of a command-8 attack | Kernel `cameraChange` plus actor section 6 |
| Camera during the visual effect | Effect initializer, camera block/script, or procedural tasks |
| Target-dependent framing | Camera script's use of `C3 15` and coordinate modes |
| Opening-shot frequency | Camera Movement setting and request gates |
| Camera remaining after the effect | Script/effect flags and return-view cleanup |

## Function addresses

| Function / site | Address | Role |
|---|---|---|
| `MonsterAI` selected-entry reads | `0x489823-0x48982C` | Command, ability ID, actor sequence |
| `computeCommandAction` | `0x48D200` | Builds the action; resolves kernel effect/camera inputs |
| `getMonsterCameraCategory` | `0x48B9F0` | Reads section 7 camera category |
| `initAnimationSequenceAtStartBattle` | `0x5027D0` | Initializes base sequence and category |
| `BS_GetCameraAnimationPointer` | `0x503520` | Resolves a collection index and queues playback |
| `ProcessCameraAnimation` | `0x5035E0` | Advances/interpolates camera keyframes |
| `BS_Camera_ReadAnimation` | `0x503C70` | Reads a camera block; initial `0xFFFF` ends it |
| `updateBattleCamera` | `0x504060` | Camera VM, tasks, render-facing output, return view |
| `someResetBattleStateEntity` | `0x505BC0` | Starts an actor sequence without replacing its saved base |
| `sub_505F00` | `0x505F00` | Opening-camera request gate |
| `au_re_BS_GetRandomCamera_Probably` | `0x5060E0` | Shared-branch frequency and encounter/model exclusions |
| `cameraWhenDoingAction` | `0x506190` | Per-command opening-camera selection |
| Monster base/sequence test | `0x506283` | Monster 0/1 index choice |
| `battle_monster_dat_loader` | `0x507120` | Binds monster sections, including its camera collection |
| `BS_UpdateCameraSequence` | `0x509610` | Camera-setting byte-code driver |
| `CameraSeq_ReadSpecialVar_C3` | `0x509640` | Camera context/category reads |
| `BS_GetCameraHeaderPointers` | `0x509970` | Installs a full block's script/collection pointers |
| `Battle_PlayCameraAnimation` | `0x5099A0` | Starts an effect/stage camera block |
| `BattleTask68_DispatchActionSequence` | `0x50A790` | Chooses the action handler |
| `BattleActionSequence_Tick_MagicCast` | `0x50A9A0` | Actor casting sequence, opening shot, then effect |
| `BS_Camera_ArmReturnAfterEffect` | `0x50A730` | Arms return-view handling |
| `Magic_EffectEnd_ResetCameraAndEntityFlags` | `0x50AED0` | Conditional return and cleanup |
| `Magic_GetIDLoad` | `0x50AF20` | Resolves the visual-effect implementation |
| `BattleTask68_LoadActionContext` | `0x50BF90` | Loads action/target context |
