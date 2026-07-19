---
layout: default
parent: Battle
title: victory Sequence (r0win.dat)
author: MakiPL, lodrot, HobbitDur
permalink: /technical-reference/battle/victory-sequence-r0windat/
---

1. TOC
{:toc}

## Overview

**R0WIN.DAT** holds the battle **victory ("win pose") sequence**: the fanfare music,
the victory camera and the per-character win poses that play once a battle ends in a
win. There is a single `R0WIN.DAT` in the game; it is entry **766 (`0x2FE`)** of the
master battle-file name table (`BattleFilesArray`), sitting right at the boundary
between the `*.DAT` files and the `MAG###.X` magic-model files. It is loaded on demand
through the normal [battle file loader](../battle-files/) into the shared battle
scratch buffer (`BS_FILE_MEMORY`), exactly like the character `c0m*` models and
`b0wave.dat`.

The win poses are not baked into the character models — they are supplied by
R0WIN.DAT and *bound onto the live party entities* when the victory task runs.

The file can be edited with the **Watts** tool of
[FF8UltimateEditor](https://github.com/HobbitDur/FF8UltimateEditor) (GUI and
`python cli.py watts`): the fanfare song id, each win-pose animation sequence (the same
three-view editor as IfritSeq), the camera animation keyframes, plus win-pose replacement
from any animation of the character's own battle model.

## The common offset-table layout

The file header and every section except the camera share one little layout, a table
of `int` offsets relative to the start of the table:

| Offset          | Type | Name                                              |
| --------------- | ---- | ------------------------------------------------- |
| 0               | int  | Count (number of data blocks)                     |
| 4               | int  | Block 0 offset                                    |
| ...             | int  | ...                                               |
| 4 + 4×(Count-1) | int  | Block Count-1 offset                              |
| 4 + 4×Count     | int  | End offset (points past the last block)           |

Blocks are contiguous, ascending and 4-byte aligned; the first block starts right
after the table.

## File structure

```
HEADER  (offset table, Count = 8; its "end" entry doubles as the runtime workspace base)
SECTION 1  victory fanfare   (offset table: AKAO sample bank + AKAO music sequence)
SECTION 2  victory camera    (a standard battle camera data blob)
SECTION 3  win pose  Rinoa   (offset table: body anim + AnimSeq [+ weapon anim])
SECTION 4  win pose  Quistis
SECTION 5  win pose  Irvine
SECTION 6  win pose  Edea    (no weapon anim)
SECTION 7  win pose  Selphie
SECTION 8  win pose  Kiros   (no weapon anim)
EOF
```

In the vanilla file the header's end entry equals the file size; at runtime the region
from there on is used as a workspace: `BS_BindEntityModelFromComData` writes the
per-entity `ComFileData` structures there and advances the pointer for each bound
character.

## Loading & runtime flow

The victory sequence runs as a battle-stage task, `BS_R0win_PlayVictorySequence`. It is
a four-state machine driven by a state byte in its task node:

| State | Action                                                                                                                                                                                                                                       |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | `BattleFile_CharacterLoad(766, BS_FILE_MEMORY)` — loads `R0WIN.DAT` into the shared battle buffer, registers the async load callback, advances.                                                                                              |
| 1     | Waits for `BATTLE_FILE_LOADING_STATE >= 0` (load complete), then issues battle-music command 4 with parameter 3 (`BS_Music_SetCommand(3)`), a volume transition that ducks the battle music before the fanfare.                              |
| 2     | `BS_R0win_QueueVictoryFanfare(SECTION 1, &done_flag)` — registers the fanfare sub-block pointers and queues the fanfare playback task on the AnimSeq task queue.                                                                             |
| 3     | Waits for the fanfare task's done flag, sets the fanfare channel volume to 127, then for each of the 3 party slots binds that character's **win-pose section** (Sections 3–8) onto the entity, and plays the **victory camera** (Section 2). |

Only entities that are loaded and not in a blocking animation state (`entity_flags & 2`,
`anim_status & 0x1A == 0`) receive a pose.

### Per-character pose selection

In state 3 the handler matches each entity's [`com_id`](../battle-slot-data/) against a
small lookup table, `R0win_WinPoseComIdMap` — six `{com_id, section_field}` byte pairs
(stride 2). A match binds that character's pose section and queues chain-transformation
**1**. A **miss** queues the generic fallback chain-transformation **18** and binds
nothing.

Consequently only six characters have a dedicated victory pose inside R0WIN.DAT:

| Section   | `com_id` | Character | Body bones | Weapon bones |
| --------- | -------- | --------- | ---------- | ------------ |
| Section 3 | 4        | Rinoa     | 32         | 2            |
| Section 4 | 3        | Quistis   | 27         | 9            |
| Section 5 | 2        | Irvine    | 34         | 3            |
| Section 6 | 7        | Edea      | 35         | —            |
| Section 7 | 5        | Selphie   | 25         | 7            |
| Section 8 | 9        | Kiros     | 35         | —            |

The bone counts are those of the characters' own battle models (`dXc`/`dXw` files):
R0WIN.DAT carries **no skeleton of its own**, so its animations only decode against the
matching model's skeleton.

### Why only these six — and why the others are absent

`com_id` values not present in the table — **Squall (0), Zell (1), Seifer (6), Laguna (8),
Ward (10)** — take the fallback: `QueueChainTransformation(entity, 18)` →
`someResetBattleStateEntity` (`0x505BC0`), which calls `doesSeqExist(entity, 18)`
(`0x505850`) and, if it exists, sets the entity's `currentAnimSeqId = 18` — i.e. it
**plays animation sequence 18 from the character's own `dXw`/`dXc` model**. Sequence 18 is
the character's **"Victory Animation"** (see the
[character sequence ids](../model-sections/animation-sequences/)). (The old
"chain transformation / Ultimecia final form" annotation on that function is spurious — the
code just restarts an animation sequence.)

`doesSeqExist` returns true only when the sequence index is in range **and its offset word
is non-zero**; an empty sequence has offset 0, so it counts as *absent* and nothing plays.

R0WIN.DAT therefore exists to **fill in the victory pose for exactly the characters whose
own model does not have a usable sequence 18**. Reading each character's own sequence 18
confirms the split precisely:

| Character | In R0WIN? | Own sequence 18 (weapon/body model) |
| --------- | --------- | ----------------------------------- |
| Squall, Zell, Seifer, Laguna, Ward | no | a real victory animation: blink timeline → play a dedicated victory anim → hold. The played body-animation id is Squall/Zell **30**, Seifer/Ward **26**, Laguna **28** |
| Irvine, Rinoa, Selphie, Edea, Kiros | yes | **empty** (0 bytes → `doesSeqExist` false → nothing would play) |
| Quistis | yes | a **stub** (`00 E6 FF` — just plays the idle standing anim and holds) |

So the five absent characters already animate their own victory pose; the six present
ones have no real one (empty, or Quistis's idle stub), so R0WIN.DAT supplies a
purpose-built pose that `BS_BindEntityModelFromComData` binds over the model and plays via
chain-transformation 1.

## SECTION 1 — victory fanfare

An offset table with two blocks, handed to `BS_R0win_QueueVictoryFanfare`:

| Block | Content                                                                                                                                                          |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | **AKAO sample/instrument bank** (126,144 bytes in vanilla). On PSX this is uploaded to sound RAM; on PC the upload call is stubbed (`return_0`), so it is vestigial. |
| 1     | **AKAO music sequence** (4,280 bytes in vanilla, header `AKAO`, id 2) — the actual victory-fanfare score.                                                          |

The fanfare playback runs as its own 3-state task, `BS_R0win_PlayVictoryFanfareTask`,
queued on the battle AnimSeq task queue. Its states set battle-music commands consumed
once per frame by the battle music dispatcher `BS_Music_ProcessCommand`:

| Music command | Issued by                            | Effect                                                                                                          |
| ------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| 1             | fanfare task state 0                 | stop music channels 0 and 1; upload the sample bank (block 0) — PSX only, stubbed on PC                          |
| 2             | fanfare task state 1                 | copy the AKAO sequence (block 1) over the `AKAO_Pointer` buffer, then `PlayMusic_SdMusicPlay` starts the fanfare |
| 3             | `BS_Music_SetChannelVolumeCommand`   | set or fade the fanfare channel volume (victory task state 3 sets it to 127)                                     |
| 4             | `BS_Music_SetCommand`                | volume transition on the current music (victory task state 1 ducks the battle music with parameter 3)            |

> The old reading of this section as the "victory timeline / AnimSeq" was wrong — the
> timeline byte-code actually lives inside each pose section (see below). Section 1 is
> sound only, exactly like sections 9/10 of the monster `c0m` files
> ([sounds](../model-sections/sounds/) / [sound sample bank](../model-sections/sound-sample-bank/)).

### How much of it the PC port actually reads

On PSX both blocks are fully used (SPU bank upload + AKAO sequencing). On the PC port
**a single byte of Section 1 is meaningful**: `Music_PlayFromAKAO` scans the first 8
bytes of block 1 for the `AKAO` magic, reads the AKAO id at **byte 4**, and plays
DirectMusic song `id - 1` through `Music_PlaySegmentById` (a hardcoded list of ambient
song ids plays as looping `.wav` streams instead, and id 17 is remapped to 99 outside
field 339 — the Julia piano scene). The rest of the 4,280-byte score is never
sequenced, and the sample bank is never read at all (its upload call is the stub).

Vanilla block 1 carries AKAO id **2**, so the PC plays song 1 — the victory fanfare.
Changing that one byte swaps the victory music for any other song id
(`cli.py watts set-fanfare-id`).

## SECTION 2 — victory camera

A standard battle camera data blob (`BattleStageCameraData`), the same layout the
[battle stage .X files](../battle-stage-x/) use:

| Offset | Type | Name                | Vanilla value            |
| ------ | ---- | ------------------- | ------------------------ |
| 0      | u16  | pointerCount        | 2                        |
| 2      | u16  | offset to camera sequence (VM byte-code) | 8   |
| 4      | u16  | offset to camera animation collection    | 0x60 |
| 6      | u16  | data size           | 2884 (the section size)  |

So the blob has two halves, both relative to the section start:

- **Camera sequence** (offset 8, 88 bytes in vanilla): the [camera byte-code VM](../model-sections/camera-sequence/)
  — opcodes `00`–`09` plus the shared arithmetic/jumps. It picks which animation of the
  collection to play and how to frame it. This is the *camera setting* half.
- **Camera animation collection** (offset 0x60, 2788 bytes): the keyframed camera
  motions themselves, in the standard [camera animation collection](../model-sections/camera-sequence/)
  format — `{u16 nbOfSet; u16 setPointer[]; u16 eof}`, each set holding 8 animation
  slots, each slot a chain of control-word blocks of 18-byte keyframes (duration,
  position xyz, look-at xyz, interpolation modes). R0WIN.DAT ships **3 sets of 8
  animations** (110 keyframes total). Editable in the Watts tool.

`BS_R0win_PlayVictoryCamera` hands the whole blob to `Battle_PlayCameraAnimation`
(→ `BS_GetCameraHeaderPointers` registers both the sequence and the collection pointer)
and the normal per-frame camera driver plays it.

### Which set is used, and who chooses it

The set is **not** stored in the per-character pose sections (Sections 3–8 are only pose
models); it is chosen entirely inside the camera half of Section 2, at runtime. Every
"play camera animation" call takes a single **animation-id byte** that `BS_GetCameraAnimationPointer`
(`0x503520`) splits into `set = (id >> 4) & 0xF` (the high nibble) and `slot = id & 7`
(the low 3 bits) — 8 slots per set. So playing set 2, slot 3 means id `0x23`.

The r0win **camera sequence** (the setting half) computes that id rather than hard-coding
it. Its byte-code reads the **count of celebrating party members** (camera special read
`C3 0x13`) and one or more **random values** (`C3 0x11`), builds an id into camera local
variable 0, and plays it with `05 00` (play the animation whose id is that local
variable). Decoded, the logic is:

- **exactly 3 members celebrating** → base id `0x20` (**set 2**, the full-party framing),
  about half the time; the other half falls through to the general case below;
- **otherwise (1–2 members, and that 50 % overflow)** → a coin-flip between base id `0x00`
  (**set 0**) and `0x10` (**set 1**), each with a random slot.

So it is **not** a plain 1→set 0 / 2→set 1 / 3→set 2 mapping: set 2 is reserved for the
full trio, while sets 0 and 1 are the general random pair. Nothing in the per-character
sections influences it. The `1/8` attacker close-up below is a separate branch that
bypasses this entirely and reads from the battle stage's own camera collection.

### How one slot plays

Only that **one slot** plays (the 8 slots of a set are alternatives, not a playlist). A
slot is a chain of keyframe **blocks** terminated by `0xFFFF`, and `ProcessCameraAnimation`
(`0x5035E0`) plays the whole chain: for each block it steps `CurrentAnimationTime += 16`
per frame up to `TotalAnimationDuration = Σ(duration)×16`, with keyframe timings at
`Σ(duration)×16`, and interpolates the position and look-at:

- **1 keyframe** → static hold;
- **2 keyframes** → linear glide from the first to the second, then the second is **held**
  for its own duration;
- **3+ keyframes** → a **natural cubic spline** through them (`sub_50D060` solves the
  moments with zero second derivative at the ends, `interpolateCameraParameter` evaluates).

Timing can be eased by the block control word (`bs_camera_timeOp_unk`): `0x3C1` is linear,
`0x3C5` applies the PSX sine ease twice. FOV and roll interpolate per block as well. When
a block's time runs out `BS_Camera_ReadAnimation` loads the next block; the `0xFFFF`
terminator ends the slot. So a 2-keyframe slot is a short single glide, while a
multi-block slot is a longer multi-segment move. The Watts preview reproduces this
playback (block chaining, hold, spline, easing).

`BS_R0win_PlayVictoryCamera` has two quirks:

- it does nothing when the idle stage camera is off/ending, or on a handful of stages
  (`battle_file_id` 11 and 0x98–0x9C — the Lunatic Pandora interior stages);
- with a **1/8 chance** (`rand < 0x2000`), when the last attacker's party slot is valid,
  loaded and not in a blocking animation, it plays a **close-up on the winning attacker**
  instead: camera animation **22 or 23** (50/50) taken from the *battle stage's* own
  camera collection, not from R0WIN.DAT.

## SECTIONS 3–8 — per-character win poses

Each pose section is an offset table with 2 or 3 blocks:

| Block | Content                                                                                                                                          |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0     | **Body animation section** — same format as [monster .dat Section 3](../model-sections/model-animation/): `{u32 nbAnims=1; u32 offset}` + one bit-packed animation. All vanilla poses have **60 frames**. |
| 1     | **Animation sequence section** — same format as [monster .dat Section 5](../model-sections/animation-sequences/): `{u16 nbSeq=1; u16 offset}` + one AnimSeq byte-code stream driving the win pose. |
| 2     | **Weapon animation section** (only when the character has a separate weapon model) — same format as block 0, decoded against the weapon skeleton. Absent for Edea and Kiros. |

`BS_BindEntityModelFromComData` binds a section onto a battle entity: the entity's body
animation controller receives {block 0, block 1} and, when the entity has a weapon
animation header, the weapon controller receives block 2. The same binder is shared
with the magic/GF system for `mag*` files.

### The win-pose byte-code

The sequences are tiny and all follow the same pattern — Rinoa's, disassembled:

```
9F 13 15 2C 30 35 39 FF   Blink timeline: toggle eye texture anim, each byte = frame delay, FF ends
00                        Play anim 0 (the 60-frame win pose) and wait for it to end
A9                        End sequence (hard stop): bake current transforms
E6 FF                     Jump -1: hold here
```

Irvine's and Selphie's sequences skip the blink timeline (`00 A9 E6 FF` only); the
blink byte lists differ per character. This is where the "victory timeline" really
lives — one sequence per character, not a global one.

## Function & symbol reference

For readers following along in IDA. Names below are the ones set in the shared IDA
database (FF8 2013 PC, `FF8_EN.exe`, ImageBase `0x400000`).

| Name                               | Address    | Role                                                                                                 |
| ---------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| `BS_R0win_PlayVictorySequence`     | `0x503040` | The victory-sequence task; loads R0WIN.DAT, ducks the music, queues the fanfare, binds poses/camera. |
| `BattleFile_CharacterLoad`         | `0x508480` | Wrapper over the battle file loader used with index 766.                                             |
| `LoadBattleFile`                   | `0x482610` | Resolves `BattleFilesArray[id]`, opens from the battle folder / `data\battle`, loads into a buffer.  |
| `BS_R0win_QueueVictoryFanfare`     | `0x501A20` | Registers Section 1's sample-bank/sequence pointers and queues the fanfare task.                     |
| `BS_R0win_PlayVictoryFanfareTask`  | `0x501A70` | 3-state fanfare playback task: bank upload command, sequence copy + play command, done flag.         |
| `BS_Music_ProcessCommand`          | `0x501B60` | Battle music command dispatcher (commands 1–4 above), consumed once per frame.                       |
| `BS_Music_SetChannelVolumeCommand` | `0x501B10` | Issues music command 3 (set/fade fanfare channel volume).                                            |
| `BS_Music_SetCommand`              | `0x501B40` | Issues music command 4 (volume transition; parameter 3 ducks the battle music).                      |
| `PlayMusic_SdMusicPlay`            | `0x46B510` | Entry point of AKAO playback on PC (wraps `Music_PlayFromAKAO`).                                     |
| `Music_PlayFromAKAO`               | `0x46B530` | Reads only the AKAO id (byte 4) and plays DirectMusic song `id - 1`, or a looped ambient .wav.       |
| `Music_PlaySegmentById`            | `0x46C2A0` | Plays a DirectMusic `.sgt` segment by song id.                                                       |
| `BS_BindEntityModelFromComData`    | `0x5022C0` | Generic bind of an animation+sequence block onto a battle entity (shared across battle/magic).       |
| `BS_R0win_PlayVictoryCamera`       | `0x5064F0` | Plays the Section 2 camera, or the 1/8-chance attacker close-up (stage camera anims 22/23).          |
| `Battle_PlayCameraAnimation`       | `0x5099A0` | Registers a camera data blob's sequence/animation pointers and starts the sequence.                  |
| `BS_GetCameraHeaderPointers`       | `0x509970` | Resolves the blob's two relative offsets into the live camera pointers.                              |
| `BattleFilesArray`                 | `0xB84CCC` | Master battle-file name pointer table; entry 766 → `"R0WIN.DAT"`.                                    |
| `aR0winDat`                        | `0xB83C58` | The `"R0WIN.DAT"` filename string.                                                                   |
| `R0win_WinPoseComIdMap`            | `0xB8B7E0` | 6× `{com_id, section_field}` pairs (com_id → pose section).                                          |
| `R0win_WinPoseSectionField`        | `0xB8B7E1` | Interleaved "section field" column of the map (stride 2).                                            |
| `R0win_WinPoseComIdMap_End`        | `0xB8B7EC` | End marker used as the map's loop bound.                                                             |
| `AKAO_Pointer`                     | `0x1CE075C`| Buffer the fanfare AKAO sequence is copied into before playback (`Pointer_AKAOPointer` points at it).|

Local IDA types added: `R0winFileHeader` (the header offset table) and
`R0winWinPoseMapEntry` (`{ u8 com_id; u8 win_section_field; }`).
