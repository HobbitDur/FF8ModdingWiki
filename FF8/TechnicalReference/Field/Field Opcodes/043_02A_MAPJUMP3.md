---
layout: default
parent: Field Opcodes
title: 02A_MAPJUMP3
nav_order: 43
permalink: /technical-reference/field/field-opcodes/02a-mapjump3/
---

-   Opcode: **0x02A**
-   Short name: **MAPJUMP3**
-   Long name: Jump to map

#### Argument

Destination walkmesh triangle ID (16-bit; stored to `wm2field_FieldZ`).

#### Stack

  
*Destination Field Map ID*

*XCoord*

*YCoord*

*(extra parameter)*

*Facing direction*

**MAPJUMP3**

#### Description

Same as [MAPJUMP](../029-mapjump/) but pops one extra value. The five stack values are, from the top: facing direction (`wm2field_FieldTarget`), an extra parameter stored to `wm2field_UnusedJumpParam`, the Y then X spawn coordinates (`wm2field_FieldY`/`wm2field_FieldX`), and last the destination field map ID (`MenuState_opcode_menu_id`). The inline 16-bit argument is the walkmesh triangle to spawn on, in the destination field's `.id` (`wm2field_FieldZ`). It sets the low byte of `globalFieldNextModuleID` to 1 to request the field change next frame, then returns 1.

The extra value was historically guessed to be a facing angle (never above 360, usually a multiple of 4). On PC, `wm2field_UnusedJumpParam` is only written (by MAPJUMP3 and [DISCJUMP](../038-discjump/)) and never read, so the value has no effect.

PC handler: `SCRIPT_MAPJUMP3`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MAPJUMP3` | 0x521AC0 | Field script opcode handler (verified IDA function) |
