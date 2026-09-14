---
layout: default
parent: Field Opcodes
title: 029_MAPJUMP
nav_order: 42
permalink: /technical-reference/field/field-opcodes/029-mapjump/
---

-   Opcode: **0x029**
-   Short name: **MAPJUMP**
-   Long name: Jump to map

#### Argument

Destination walkmesh triangle ID (16-bit; stored to `wm2field_FieldZ`).

#### Stack

  
*Destination Field Map ID*

*XCoord*

*YCoord*

*Facing direction*

**MAPJUMP**

#### Description

Jump the player to another field. The handler pops four values from the stack: the facing direction (top of stack, `wm2field_FieldTarget`), the Y then X spawn coordinates (`wm2field_FieldY`/`wm2field_FieldX`), and last the destination field map ID (`MenuState_opcode_menu_id`, which becomes `CURRENT_FIELD_ID`). The inline 16-bit argument is the walkmesh triangle to spawn on, in the destination field's `.id` (`wm2field_FieldZ`). It then sets the low byte of `globalFieldNextModuleID` to 1, which requests the field module to load the new map next frame. Returns 1 (wait).

These are the same globals a walked exit fills from its [gateway record](../../field-file-format/field-gateways/), and the same ones a saved game fills on load (`FFNewGame_or_load`: `SG_COORD_X/Y_PARTY_1`, `SG_TRIANGLE_PARTY_1`, `SG_DIRECTION_PARTY_1`, `SG_CURRENT_FIELD`), which is how their meaning is confirmed.

PC handler: `SCRIPT_MAPJUMP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MAPJUMP` | 0x521A20 | Field script opcode handler (verified IDA function) |
