---
title: Camera sequence
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/camera-sequence/
nav_order: 6
author: HobbitDur
---

## Camera sequence

The camera sequences reuse the **same byte-code VM** as [animation sequences](../animation-sequences/) (arithmetic `C0`-`E5` and jumps `E6`-`F3` behave identically), with camera-specific
callbacks (`CameraSeq_DispatchActionOpcode`, driver `BS_UpdateCameraSequence`).

### Two container forms (important)

Camera data ships in **two container shapes**, and they are easy to confuse because both open with a `u16 count + u16 pointer table`:

- **Full camera blob with a byte-code setting** — battle-stage `.X` files, R0WIN section 2, and spell/effect camera globals (`MAG_*`). An 8-byte header (`pointerCount`, relative offset to the **camera setting** = the byte-code VM sequence, relative offset to the **camera animation collection**, size), then the camera-setting byte-code (e.g. `a0stg000.x`: `05 00 C3 10 E5 7F C1 00 CB 7F EA 06 …`), then the collection. This is the [`BattleStageCameraData`](../../file-format-x/#camera-data) layout, and **this is the only form that contains a byte-code camera sequence.** Started via `Battle_PlayCameraAnimation`.
- **Bare camera animation collection** — **per-entity cameras: monster files section 6, and character files (`dXc`) section 5**. There is **no 8-byte header and no camera-setting byte-code**: the section *is* a [camera animation collection](../../file-format-x/#camera-animations-collection) and starts directly at `NumOfSets`, ending with an EOF word equal to the section's byte length. The engine plays these through `cameraWhenDoingAction`, which passes the *acting entity's own* collection pointer (`command_queue->camera_animation_collection`, at offset 0x2C of the command-queue struct, set at load time to the entity's section-6/section-5 destination — see `Battle_isLoadSquallEtc` @0x5078CA) to `BS_GetCameraAnimationPointer`. Verified:
  - **Monsters** — over all `c0m*.dat`: 133 files are a valid bare collection (`NumOfSets` usually **1** → 8 slots), 66 empty, 0 malformed.
  - **Characters** — all 17 `dXc` section-5 blocks parse with the *same* parser: `NumOfSets = 2` (16 slots, 8 per set), `EOF == section length`, every pointer resolves. What looks like an 8-byte blob header (`02 00 08 00 08 04 b8 06`) is really the collection header itself: `NumOfSets = 2`, `setPtr[0] = 0x08`, `setPtr[1] = 0x408`, `EOF = 0x6B8` (= 1720 = length). **Characters carry no camera byte-code** — like monsters, their "which shot / how" logic lives outside the file (in `cameraWhenDoingAction`).

In other words: the opcodes and the C3/E5 tables below describe the **byte-code half**, which only the stage/R0WIN/spell blobs carry. A per-entity camera section (monster §6 or character §5) is purely the key-framed collection (positions, look-at, FOV, roll) that the `00`/`05` opcodes would play. The [FF8UltimateEditor](https://github.com/HobbitDur/FF8UltimateEditor) *Camera* tab edits these collections directly; the same collection parser handles both the monster (1-set) and character (2-set) cases.

### Who starts a camera sequence

A camera data blob starts with a small header containing two relative offsets: one to the **camera sequence** (the VM byte-code interpreted here) and one to the **camera animation collection** (the actual key-framed camera motions that opcodes `00`/`05` play).

A camera sequence is started by calling `Battle_PlayCameraAnimation` with a pointer to such a blob, which registers both pointers (`CURRENT_CAMERA_SETTING_ADDR` / `CURRENT_CAMERA_ANIMATION_COLLECTION_HEADER_ADDR`). In practice this is called:

- at battle start by `BS_CameraInit` (the battle stage's idle camera),
- by **every spell/ability effect routine** (the `MAG_xxx` functions in magic.fs and the monster-attack effect inits) when the action's visual effect begins — each effect embeds/points to its own camera data. For monster abilities the camera comes from this section.

A camera sequence can adapt its framing to the monster it is filming through the [camera category](../information-stats/#byte-246-camera-category) ([information & stats](../information-stats/) byte 246): that per-monster value is converted at battle start into the entity's camera variable, which camera sequences read back via camera-C3 `0x15` (see the table below).

From then on, the battle camera update (`updateBattleCamera`, every frame unless battle is paused) calls `BS_UpdateCameraSequence`, which interprets the sequence: it runs until opcode `01` (yield, one frame), and stops when it reaches `02` (or any unknown opcode), releasing the camera back to the default behaviour.

Camera opcodes < 0xC0:

| Opcode | Params | Description                                                                         |
|--------|--------|---------------------------------------------------------------------------------------|
| 00 XX  | 1      | Play camera animation XX from the current camera animation collection               |
| 01     | 0      | Yield (pause for this frame, resume next frame)                                     |
| 02     | 0      | End the camera sequence and clear the camera pointer                                |
| 03     | 0      | Capture the current camera pose as the idle/rest pose (copies the live position/look-at into the default-pose registers) + clear flag bit 15 |
| 04 XX  | 1      | Start a camera oscillation (wobble) task with param XX                              |
| 05 XX  | 1      | Play camera animation whose id is read through the camera special-value reader (XX) |
| 06     | 0      | Set camera flag bit 15                                                              |
| 07     | 0      | Clear camera flag bit 15                                                            |
| 08     | 0      | Reset the wobble factor (4096) and the camera flag                                  |
| 09 XX  | 1      | Nop (parameter skipped)                                                             |
| other  | -      | Reset wobble factor and end the sequence                                            |

Camera C3-family special reads (`CameraSeq_ReadSpecialVar_C3`):

| Param     | Value read                                                       |
|-----------|---------------------------------------------------------------------|
| 0x00-0x07 | Camera animation local variables                                 |
| 0x10      | Camera flag variable                                             |
| 0x11      | Random value                                                     |
| 0x13      | Count of party members in a specific animation state             |
| 0x15      | Target entity's camera var: its [camera category](../information-stats/#byte-246-camera-category) ([information & stats](../information-stats/) byte 246), also overridable at runtime by entity sequences via E5 0x2B |
| 0x16      | Target's animation status (with dead-flag fixup)                 |
| 0x17      | Battle task value                                                |
| 0x18      | Attacker slot id                                                 |
| 0x19      | Target slot id                                                   |
| 0x1A      | Number of affected targets                                       |
| 0x1B      | Count of party members with animation status 0                   |
| 0x1C-0x22 | Random value modulo 2..8                                         |
| > 0x77    | Camera stack (same principle as the entity stack)                |

Camera E5 writes: params < 8 write the camera animation local variables, 0x10 writes the camera flag variable, > 0x77 writes the camera stack.

## Function addresses

FF8_EN.exe:

| Function | Address | Description |
|---|---|---|
| `CameraSeq_DispatchActionOpcode` | 0x509810 | Camera-sequence opcode dispatcher (verified IDA function) |
| `BS_UpdateCameraSequence` | 0x509610 | Per-frame driver for the active camera sequence (verified IDA function) |
| `Battle_PlayCameraAnimation` | 0x5099A0 | Registers a camera data blob's sequence/animation pointers and starts the sequence (verified IDA function) |
| `updateBattleCamera` | 0x504060 | Per-frame battle camera update; calls `BS_UpdateCameraSequence` (verified IDA function) |
| Camera pose capture routine (`sub_503300` in IDA, unnamed) | 0x503300 | Copies the live camera position/look-at into the default-pose registers, used by opcode `03` (verified IDA function) |
| Default-pose registers | 0xB8B800 | Global data holding the idle/rest camera pose (Global variable/data, not a function) |
| `CameraSeq_ReadSpecialVar_C3` | 0x509640 | Camera C3-family special-variable reader (verified IDA function; also referenced as `a3ParamAnimSeqForCamera` — an older name — on the [Information & stats](../information-stats/#function-address-reference) page) |
