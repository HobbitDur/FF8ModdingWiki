---
layout: default
title: Field script entity structure
parent: Field
permalink: /technical-reference/field/entity-struct/
---

1. TOC
{:toc}

# Field script entity structure

The in-memory structure behind every field actor — the script-VM state plus (for characters) the model/position/movement data. This is what the field script opcodes (`a1` = the entity) and the field runtime read and write. Addresses for FF8_EN.exe, image base 0x400000.

## Two-level layout

`FieldEntityHeader` (389 bytes) is a **shared script-VM header** nested at offset 0 of four entity kinds; the field VM (`field_script_vm_run_frame` / `fieldScriptCall`) iterates all four through their `entityHeader`:

| Entity type | Size | Used for |
|-------------|------|----------|
| `FieldSpecialEntity` | — | special/background scripts |
| `FielObjectEntity` | — | field objects |
| `FieldCharacterEntity416` | 416 | NPCs |
| `FieldCharacterEntity612` | 612 | playable characters (full model + walkmesh) |

The model/position/movement/walkmesh region is **specific to the 612-byte character entity** — it is not part of the shared header (extending the header would corrupt the smaller layouts).

## Script header (`FieldEntityHeader`, 0x000–0x184)

Each entity runs up to **8 concurrent script threads by priority** (0 = highest). The header holds the eval stack, the per-priority instruction pointers, and the current thread state.

| Offset | Type | Name | Meaning |
|--------|------|------|---------|
| 0x000 | u32[80] | `stack_data` | script argument / evaluation stack |
| 0x140 | u32 | `return_value` | last opcode return value |
| 0x144 | u32 | `opcode_status` | opcode execution status |
| 0x148–0x15F | u32[6] | *(unknown)* | 6 dwords, unreferenced in the VM/RET/movement code — still unidentified |
| 0x160 | u32 | `execution_flags` | per-thread state flags (movement/anim/wait bits) |
| 0x164 | u16[8] | `script_ip_per_priority` | saved instruction pointer per priority slot |
| 0x174 | u8 | `ready_bit_index` | current priority level (0–7) |
| 0x175 | u8 | `opcode_ready_mask` | bitmask of priorities ready to run (the gate every opcode checks) |
| 0x176 | u16 | `instructions_current_position` | current thread's script IP |
| 0x178 | u32 | `script_entrypoint_base` | base index into the field-script entry-point table (`base + event_id`) |
| 0x17C | u8[8] | `stack_base_per_priority` | stack base pointer per priority (on entry SP = base + 8) |
| 0x184 | u8 | `stack_current_position` | current stack pointer |

Standard opcode prologue: an opcode only runs when `(1 << ready_bit_index) & opcode_ready_mask` is set; `RET`/`RETTO` (`SCRIPT_RET`) writes 0xFFFF into `script_ip_per_priority[prio]` and restores the highest still-active priority into `instructions_current_position`.

## Character entity extras (`FieldCharacterEntity612`, 0x190–0x243)

Selected fields of the model/movement/walkmesh region (the header occupies 0x000–0x184):

| Offset | Type | Name | Meaning |
|--------|------|------|---------|
| 0x190 | s32×3 | `pos_x/y/z` | **live walkmesh position** (fixed-point ≫12), committed by `Field_Walkmesh_MoveEntityStep` |
| 0x19C | s32×3 | `pos_jump_start_x/y/z` | position saved at jump start |
| 0x1B4 | s32×3 | `move_pos_x/y/z` | scripted-MOVE current position |
| 0x1C0 | s32×3 | `move_target_x/y/z` | scripted-MOVE target (RETTO restores current ← target) |
| 0x1D8 | u16×2 | `move_duration_frames` / `move_frame_counter` | MOVE/JUMP tween counters |
| 0x1DC | u16×2 | `turn_lerp_from/to` | TURN/DIR angle tween endpoints |
| 0x1E0/1E6/1EC | s16 | `model_offset_x/y/z` | draw offsets added to `pos ≫ 12` |
| 0x1F6 | u16 | `collision_radius` | collision/interaction feeler radius (default 48 on load) |
| 0x1FA | u16 | `current_triangle` | current walkmesh triangle index |
| 0x1FE/202 | u16 | `move_speed` / `move_speed_saved` | per-frame movement speed |
| 0x206–0x20C | u16 | `anim_frame_current/step/loop/count` | idle-animation frame stepping |
| 0x218 | s16 | `model_id` | model id |
| 0x21A/21C | u16 | `move_angle_current/saved` | |
| 0x21E | u16 | `motion_substate` | jump/move sub-phase |
| 0x222–0x236 | s16 | `headlook_target_x/y/z`, pitch/yaw/frames | head-tracking block (`SetModelPoseAndHeadLook`) |
| 0x238/23A/23B | u8 | `headlook_max_pitch/max_yaw/active` | |
| 0x23C | u8 | `motion_state` | 0 = idle, 1 = jump, 3 = ladder, 4 = special |
| 0x23F | u8 | `facing_angle` | movement/input facing (sin/cos source) |
| 0x241 | u8 | `model_facing_angle` | rendered/tweened facing |
| 0x249/24B/24C | u8 | `pushonoff` / `talkonoff` / `throughonoff` | collision/interaction toggles |
| 0x24E | u8 | `current_anim_id` | currently displayed base animation |
| 0x24F… | u8 | `baseanim1/2/3`, `ladderanim1-3` | idle / walk / run and ladder animation ids |
| 0x256 | u8 | `model_instance_idx` | index into `CHARA_MODEL_INSTANCE_TABLE` |

## Corrections to earlier notes

Mapping this struct corrected several offsets that had been guessed from partial reads:

* The **live walkmesh position is at 0x190** (400), not +484 — the +484 triple is `model_offset_x/y/z` (draw offsets). Position exists once.
* **Collision radius is at 0x1F6** (502), not +586 (which is a talk-event trigger request).
* The +436/+448 triples are the secondary **MOVE-interpolation buffers** (`move_pos`/`move_target`), not a duplicate of the live position.
* The +572 byte is a multi-value **`motion_state`** (0/1/3/4), not a boolean "moving" flag.

## Open item

`FieldEntityHeader` offsets **0x148–0x15F** (6 dwords) remain unidentified — they are not referenced by the VM dispatcher, `SCRIPT_RET`, or the movement/model functions inspected. They are likely written during field/script initialization; chasing their writers is the remaining work on this struct.

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_RET` | 0x51C5C0 | RET/RETTO opcode handler |
