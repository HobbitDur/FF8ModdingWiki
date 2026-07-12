---
title: Section 6 - Camera sequence
layout: default
parent: Monster files (c0mxxx.dat)
permalink: /technical-reference/battle/monster-files-c0mxxxdat/section-6-camera-sequence/
nav_order: 6
---

## Section 6: Camera sequence

The camera sequences reuse the **same byte-code VM** as [section 5](../section-5-animation-sequences/) (arithmetic `C0`-`E5` and jumps `E6`-`F3` behave identically), with camera-specific
callbacks (`CameraSeq_DispatchActionOpcode` at `0x509810`, driver `BS_UpdateCameraSequence` at `0x509610`).

### Who starts a camera sequence

A camera data blob starts with a small header containing two relative offsets: one to the **camera sequence** (the VM byte-code interpreted here) and one to the **camera animation collection** (the actual key-framed camera motions that opcodes `00`/`05` play).

A camera sequence is started by calling `Battle_PlayCameraAnimation` (`0x5099A0`) with a pointer to such a blob, which registers both pointers (`CURRENT_CAMERA_SETTING_ADDR` / `CURRENT_CAMERA_ANIMATION_COLLECTION_HEADER_ADDR`). In practice this is called:

- at battle start by `BS_CameraInit` (the battle stage's idle camera),
- by **every spell/ability effect routine** (the `MAG_xxx` functions in magic.fs and the monster-attack effect inits) when the action's visual effect begins — each effect embeds/points to its own camera data. For monster abilities the camera comes from this section 6; the ability's *camera flag* byte in [section 7](../section-7-informations-stats/) selects the camera behaviour.

From then on, the battle camera update (`updateBattleCamera` at `0x504060`, every frame unless battle is paused) calls `BS_UpdateCameraSequence`, which interprets the sequence: it runs until opcode `01` (yield, one frame), and stops when it reaches `02` (or any unknown opcode), releasing the camera back to the default behaviour.

Camera opcodes < 0xC0:

| Opcode | Params | Description                                                                         |
|--------|--------|---------------------------------------------------------------------------------------|
| 00 XX  | 1      | Play camera animation XX from the current camera animation collection               |
| 01     | 0      | Yield (pause for this frame, resume next frame)                                     |
| 02     | 0      | End the camera sequence and clear the camera pointer                                |
| 03     | 0      | Capture the current camera pose as the idle/rest pose (`0x503300` copies the live position/look-at into the default-pose registers at `0xB8B800`) + clear flag bit 15 |
| 04 XX  | 1      | Start a camera oscillation (wobble) task with param XX                              |
| 05 XX  | 1      | Play camera animation whose id is read through the camera special-value reader (XX) |
| 06     | 0      | Set camera flag bit 15                                                              |
| 07     | 0      | Clear camera flag bit 15                                                            |
| 08     | 0      | Reset the wobble factor (4096) and the camera flag                                  |
| 09 XX  | 1      | Nop (parameter skipped)                                                             |
| other  | -      | Reset wobble factor and end the sequence                                            |

Camera C3-family special reads (`CameraSeq_ReadSpecialVar_C3` at `0x509640`):

| Param     | Value read                                                       |
|-----------|---------------------------------------------------------------------|
| 0x00-0x07 | Camera animation local variables                                 |
| 0x10      | Camera flag variable                                             |
| 0x11      | Random value                                                     |
| 0x13      | Count of party members in a specific animation state             |
| 0x15      | Target entity's camera var (set by entity sequences via E5 0x2B) |
| 0x16      | Target's animation status (with dead-flag fixup)                 |
| 0x17      | Battle task value                                                |
| 0x18      | Attacker slot id                                                 |
| 0x19      | Target slot id                                                   |
| 0x1A      | Number of affected targets                                       |
| 0x1B      | Count of party members with animation status 0                   |
| 0x1C-0x22 | Random value modulo 2..8                                         |
| > 0x77    | Camera stack (same principle as the entity stack)                |

Camera E5 writes: params < 8 write the camera animation local variables, 0x10 writes the camera flag variable, > 0x77 writes the camera stack.
