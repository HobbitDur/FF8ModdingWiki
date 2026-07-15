---
layout: default
title: WorldMap script VM
parent: WorldMap
permalink: /technical-reference/worldmap/script-vm/
---

1. TOC
{:toc}

# WorldMap script VM

The world map has its own small event-script bytecode, stored in the [wmset]({{ site.baseurl }}/technical-reference/worldmap/worldmap-wmset/) file and evaluated every frame by the [module director]({{ site.baseurl }}/technical-reference/worldmap/module-runtime/). It drives everything scripted on the world map: conditional field warps (docks, stations, Garden/Ragnarok boarding), forced battles, docking sequences, savemap flag updates, even item rewards.

Two wmset sections contain scripts:

* **Section 37** — the global event list, evaluated every frame by `Wm_Script_RunGlobalEvents`. The section starts with an offset table (one 32-bit offset per script, terminated by 0); every script is evaluated each frame.
* **Section 8** — per-location scripts, evaluated when the player stands on a location entry that has flag bit 8 set (`Wm_Script_GetLocationWarpEntrance`), and also in a "wildcard" mode used to query what a location could trigger (`Wm_Script_GetLocationWarpAnyState`).

## Instruction format

Every instruction is 4 bytes: a signed 16-bit opcode (always `0xFFxx`, i.e. negative) followed by one 16-bit argument, or two 8-bit arguments (noted b2 = byte at +2, b3 = byte at +3). Anything that is not a known opcode terminates an action list.

## Script structure

`Wmset_warpConditionSystem` (the interpreter) walks the instructions as an IF/THEN/ELSE machine and returns a pointer to the first **action** of a branch whose conditions all passed — the caller executes the actions:

```
FF0A IF
FF01 <condition>      ; each condition prefixed by FF01
FF01 <condition>
FF0B THEN
     <actions...>
FF05 END-ACTIONS      ; also acts as ELSE boundary
FF0C ELSE-IF          ; re-evaluate after a failed IF
FF0D ELSE             ; actions if previous conditions failed
FF04 THEN-ALWAYS      ; unconditional action block
FF0E JMP offset       ; jump within the script blob
FF16 END-SCRIPT       ; next script (section 37) / stop (section 8)
```

## Condition opcodes (`wm_scriptCheckCondition`)

Returns 1 (true), −1 (false), or 0 (not a condition → treated as an action by the interpreter). The four `wm_script_override_*` globals force vehicle/position/flag/button conditions to true; they are set temporarily by `Wm_Script_GetLocationWarpAnyState`.

| Op | Test |
|------|------|
| FF02 | story progress (`world_story_progress`) >= arg |
| FF03 | story progress < arg |
| FF06 | current region (`wm_GetRegionNumber`) == arg |
| FF07 | current 2048-unit map square == arg (index = sqX + sqY×128) |
| FF09 | vehicle class check (see below) |
| FF0F / FF10 | X / Y position **within segment** (& 0x1FFF) < arg |
| FF11 / FF12 | X / Y position within segment > arg |
| FF17 | a visible instance of world object model `arg` is close to the camera |
| FF18 | docking sequence **completed** for vehicle arg (state 6 = Ragnarok/50, state 9 = Garden/48) |
| FF19 | docking sequence **in progress** for vehicle arg (state 5 = Ragnarok landing, 8 = Garden descent) |
| FF1A | touched object's model == arg |
| FF1B | touched object's model == arg and it is not one of the 8 reserved vehicle slots |
| FF1C | nearest-object model == arg, player facing it (angle diff ≤ 512) |
| FF1D | same as FF1C plus not-a-vehicle-slot check |
| FF1E | always false |
| FF20 | button pressed this frame (arg = mask, −1 = any incl. stick deflection > 45) |
| FF21 | savemap world flag bit 0 == arg |
| FF22 | current location entry index == arg |
| FF25 | `world_docking_state` context byte == arg |
| FF27 | savemap script **bit** b2 (0–63) == b3 |
| FF29 | ask-window `arg` has a chosen answer (stores it in `wm_msgwin_last_choice`) |
| FF2A | stored answer choice == arg |
| FF2C | (message window slot b2 still open) == b3 |
| FF2D / FF30 / FF31 | savemap script **var** [b2] == / > / < b3 |
| FF2F | random 16-bit (2 × `Wm_Random8` draws) < arg (probability roll) |
| FF13/FF14 | spawn world object (b2 = model class, b3 = wmset position record) — evaluated at map load |
| FF32 | location entry flag bit 8 (inverted) == arg |
| FF33 | location entry byte +13 == b2 |
| FF34 | last battle scene ID (`COMBAT_SCENE_ID`) == arg |
| FF35 | (battle result == escaped) == arg |
| FF38 | (player currently moving) == arg |
| FF39 | `SG_UNKNOWN_BATTLE_VAR` == arg |

Vehicle classes for FF09: 33/48/49/50 exact match (48 = Balamb Garden, 49 = chocobo, 50 = Ragnarok); 128 = on foot (id < 10 or 128); 129 = id < 2; 130 = id 8–9; 131 = trains (id 16–22); 132 = cars (32–40 or 132); 133 = id 34–40.

## Action opcodes (`Wm_Script_RunGlobalEvents`)

| Op | Action |
|------|--------|
| FF08 | **Warp to field** — arg = `wm2field.tbl` entrance; director returns 1 |
| FF2B | **Start battle** — arg = encounter ID; director returns 3 |
| FF26 | set `world_docking_state` context byte = b2 (starts docking sequences) |
| FF28 | set savemap script bit b2 (0–63) to b3 |
| FF2E | set savemap script var [b2] = b3 |
| FF37 | add item b2 × quantity b3 to inventory |
| FF36 | consume this frame's input (blocks further button conditions) |
| FF1F | **show message window** — slot b2, text id b3 (text from the wmset text section) |
| FF23 | **show question window** — slot b2, text id b3, 2 selectable lines (read back with FF29/FF2A) |
| FF24 | close message window slot |
| FF05 | end of action list |

The world map has 13 message-window slots (`world_msg_windows`, 16 bytes each: text id, alignment mode 0–3, text-layer handle, color, x, y). This is the system behind train-station dialogs, rental-car fare messages and the "Fuel: N" display.

The savemap script bits (2×32) and vars (2 bytes) live in the world-map save block (`SG_WORLDMAP_DATA` +116/+120 and +124) — they persist in save files.

## Function addresses

| Function | Address | Description |
|------|---------|-------------|
| `Wmset_warpConditionSystem` | 0x545F10 | Script interpreter (IF/THEN/ELSE walker) |
| `wm_scriptCheckCondition` | 0x546100 | Condition opcode evaluator |
| `Wm_Script_RunGlobalEvents` | 0x54D7E0 | Section 37 per-frame evaluation + action execution |
| `Wm_Script_GetLocationWarpEntrance` | 0x545EA0 | Section 8 script for the current location |
| `Wm_Script_GetLocationWarpAnyState` | 0x54FFE0 | Section 8 with all overrides forced true |
| `wm_script_override_vehicle/position/flag0/buttons` | 0x2040A2C–0x2040A38 | Condition wildcard flags |
| `wm_script_input_consumed` | 0x2040A40 | Set by FF36, blocks FF20 until cleared |
| `world_story_progress` | 0x2036BDE | Story progress value tested by FF02/FF03 |
| `world_docking_state` | 0x2036B70 | Docking context (see module runtime page) |
| `COMBAT_SCENE_ID` | — | Last encounter ID (FF34) |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
