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

**R0WIN.DAT** holds the battle **victory ("win pose") sequence**: the animation, camera
and per-character poses that play once a battle ends in a win. There is a single
`R0WIN.DAT` in the game; it is entry **766 (`0x2FE`)** of the master battle-file name
table (`BattleFilesArray`), sitting right at the boundary between the `*.DAT` files and
the `MAG###.X` magic-model files. It is loaded on demand through the normal
[battle file loader](../battle-files/) into the shared battle scratch buffer
(`BS_FILE_MEMORY`), exactly like the character `c0m*` models and `b0wave.dat`.

The file behaves like a small **battle "com" container**: it starts with a table of
section offsets, and its per-character sections are themselves miniature model+animation
blocks that are *bound onto the live party entities* — the victory poses are not baked
into the character models, they are supplied by R0WIN.DAT.

## Loading & runtime flow

The victory sequence runs as a battle-stage task, `BS_R0win_PlayVictorySequence`. It is a
four-state machine driven by a state byte in its task node:

| State | Action                                                                                                                                                                                                                                    |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | `BattleFile_CharacterLoad(766, BS_FILE_MEMORY)` — loads `R0WIN.DAT` into the shared battle buffer, registers the async load callback, advances.                                                                                           |
| 1     | Waits for `BATTLE_FILE_LOADING_STATE >= 0` (load complete), then activates the victory animation/timeline controller.                                                                                                                     |
| 2     | Feeds **Section 1** (`ENTRY[1]`) to the battle **AnimSeq** task queue — this drives the scripted victory timeline.                                                                                                                        |
| 3     | For each of the 3 party slots: binds that character's **victory-pose section** (Sections 3–8) onto the entity and queues its win animation, then plays the **camera animation** from **Section 2**. Returns "done" and releases the task. |

Only entities that are loaded and not in a blocking animation state (`entity_flags & 2`,
`anim_status & 0x1A == 0`) receive a pose.

### Per-character pose selection

In state 3 the handler matches each entity's [`com_id`](../battle-slot-data/) against a
small lookup table, `R0win_WinPoseComIdMap` — six `{com_id, section_field}` byte pairs
(stride 2). A match binds `ENTRY[section_field + 1]` (i.e. one of Sections 3–8) as that
character's pose and queues chain-transformation **1**. A **miss** queues the generic
fallback chain-transformation **18** and binds nothing.

Consequently only six characters have a dedicated victory pose inside R0WIN.DAT:

| ENTRY section          | `com_id` | Character |
| ---------------------- | -------- | --------- |
| Section 3 (`ENTRY[3]`) | 4        | Rinoa     |
| Section 4 (`ENTRY[4]`) | 3        | Quistis   |
| Section 5 (`ENTRY[5]`) | 2        | Irvine    |
| Section 6 (`ENTRY[6]`) | 7        | Edea      |
| Section 7 (`ENTRY[7]`) | 5        | Selphie   |
| Section 8 (`ENTRY[8]`) | 9        | Kiros     |

`com_id` values not present in the table — **Squall (0), Zell (1), Seifer (6), Laguna (8),
Ward (10)** — fall through to the generic fallback (chain-transformation 18); their win
pose comes from their own model rather than from R0WIN.DAT.

## File structure

```
ENTRY (section-offset table)
SECTION 1  (victory timeline / AnimSeq)
SECTION 2  (camera animation)
SECTION 3..8 (per-character victory poses)
SECTION "to EOF" (runtime workspace)
EOF
```

### ENTRY

A table of `int` offsets relative to the start of the file. `NumberOfSections` is 8; the
last entry points past the section data and is used at runtime as a scratch/workspace base.

| Offset | Type | Name                                    |
| ------ | ---- | --------------------------------------- |
| 0      | int  | NumberOfSections (= 8)                  |
| 4      | int  | Section_1_pointer (victory timeline)    |
| 8      | int  | Section_2_pointer (camera)              |
| 12     | int  | Section_3_pointer (Rinoa pose)          |
| 16     | int  | Section_4_pointer (Quistis pose)        |
| 20     | int  | Section_5_pointer (Irvine pose)         |
| 24     | int  | Section_6_pointer (Edea pose)           |
| 28     | int  | Section_7_pointer (Selphie pose)        |
| 32     | int  | Section_8_pointer (Kiros pose)          |
| 36     | int  | Section_to_EOF (runtime workspace base) |

### SECTION 1 — victory timeline

At runtime this section is handed to the battle **AnimSeq** task queue
(`AddTaskToQueueAnimSeq`) that orchestrates the win scene. Its own little header carries
three sub-offsets (relative to the section start):

| Offset | Name | Description                             |
| ------ | ---- | --------------------------------------- |
| 0      | int  | count / flags                           |
| 4      | int  | pointer to sub-block A (timeline start) |
| 8      | int  | pointer to sub-block B                  |
| 12     | int  | (end / length reference)                |

> Note: the loader hands this section to the AnimSeq controller that streams the victory
> timeline. The win fanfare triggers along that timeline rather than being a standalone
> AKAO sound payload.

### SECTION 2 — camera animation

Played by `BS_R0win_PlayVictoryCamera`. The layout is the standard battle camera-animation
collection — see [Battle stage model file (.X)](../battle-stage-x/).

### SECTIONS 3–8 — per-character victory poses

Each of these is a self-contained mini "com" model block bound onto a party entity by
`BS_BindEntityModelFromComData`. The header is:

| Offset | Type | Name         | Description                                                                                   |
| ------ | ---- | ------------ | --------------------------------------------------------------------------------------------- |
| 0      | int  | count        | number of sub-pointers                                                                        |
| 4      | int  | geometry_ptr | skeleton / model geometry (bound to the entity anim header)                                   |
| 8      | int  | data_ptr     | secondary model data                                                                          |
| 12     | int  | anim_ptr     | animation (also used as the weapon animation source when the entity has a weapon anim header) |

Which section belongs to which character is fixed by `R0win_WinPoseComIdMap` (see the
[per-character pose selection](#per-character-pose-selection) table above).

### SECTION "to EOF"

`ENTRY[9]` (offset 36) points past the last pose section. At runtime it is used as a
**workspace base**: `BS_BindEntityModelFromComData` writes the per-entity `ComFileData`
structures into this region and advances the pointer for each bound character.

## Function & symbol reference

For readers following along in IDA. Names below are the ones set in the shared IDA
database (FF8 2013 PC, `FF8_EN.exe`, ImageBase `0x400000`).

| Name                                 | Address    | Role                                                                                                |
| ------------------------------------ | ---------- | --------------------------------------------------------------------------------------------------- |
| `BS_R0win_PlayVictorySequence`       | `0x503040` | The victory-sequence task; loads R0WIN.DAT and binds poses/camera.                                  |
| `BattleFile_CharacterLoad`           | `0x508480` | Wrapper over the battle file loader used with index 766.                                            |
| `LoadBattleFile`                     | `0x482610` | Resolves `BattleFilesArray[id]`, opens from the battle folder / `data\battle`, loads into a buffer. |
| `BS_R0win_ActivateVictoryAnimStream` | `0x501B40` | Arms the battle AnimSeq controller for the win scene (mode 4, only caller is the victory task).     |
| `sub_501A20`                         | `0x501A20` | Pushes Section 1 sub-offsets into the AnimSeq globals and queues the timeline task (shared helper). |
| `BS_BindEntityModelFromComData`      | `0x5022C0` | Generic bind of a "com" model+animation block onto a battle entity (shared across battle/magic).    |
| `BS_R0win_PlayVictoryCamera`         | `0x5064F0` | Plays the Section 2 camera animation for the win scene.                                             |
| `BattleFilesArray`                   | `0xB84CCC` | Master battle-file name pointer table; entry 766 → `"R0WIN.DAT"`.                                   |
| `aR0winDat`                          | `0xB83C58` | The `"R0WIN.DAT"` filename string.                                                                  |
| `R0win_WinPoseComIdMap`              | `0xB8B7E0` | 6× `{com_id, section_field}` pairs (com_id → pose section).                                         |
| `R0win_WinPoseSectionField`          | `0xB8B7E1` | Interleaved "section field" column of the map (stride 2).                                           |
| `R0win_WinPoseComIdMap_End`          | `0xB8B7EC` | End marker used as the map's loop bound.                                                            |

Local IDA types added: `R0winFileHeader` (the ENTRY offset table) and
`R0winWinPoseMapEntry` (`{ u8 com_id; u8 win_section_field; }`).
