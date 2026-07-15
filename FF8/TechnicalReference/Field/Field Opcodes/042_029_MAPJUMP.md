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

Facing direction / Z on the destination field (16-bit; stored to `wm2field_FieldZ`).

#### Stack

  
*Destination Field Map ID*

*YCoord*

*XCoord*

*(entry parameter)*

**MAPJUMP**

#### Description

Jump the player to another field. The handler pops four values from the stack — the destination field map ID (top of stack, `wm2field_FieldTarget`), the Y and X spawn coordinates (`wm2field_FieldY`/`wm2field_FieldX`), and a fourth value copied to `MenuState_opcode_menu_id` — and writes the inline 16-bit argument to `wm2field_FieldZ` (the destination facing/Z). It then sets the low byte of `globalFieldNextModuleID` to 1, which requests the field module to load the new map next frame. Returns 1 (wait).

PC handler: `SCRIPT_MAPJUMP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MAPJUMP` | 0x521A20 | Field script opcode handler (verified IDA function) |
