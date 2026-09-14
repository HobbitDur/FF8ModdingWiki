---
layout: default
parent: Field Opcodes
title: 038_DISCJUMP
nav_order: 57
permalink: /technical-reference/field/field-opcodes/038-discjump/
---

-   Opcode: **0x038**
-   Short name: **DISCJUMP**
-   Long name: Disc change and map jump

#### Argument

Destination walkmesh triangle ID (stored to `wm2field_FieldZ`)

#### Stack

  
*Field Map ID*

*XCoord*

*YCoord*

*(extra parameter)*

*Facing direction*

**DISCJUMP**

#### Description

Same as [MAPJUMP3](../02a-mapjump3/), but requests a disc-change flow instead of a plain field load: it sets the low byte of `globalFieldNextModuleID` to 6 (rather than 1) and raises the `menu_disabled` flag. It pops the same five stack values, from the top: facing direction (`wm2field_FieldTarget`), an extra parameter (`wm2field_UnusedJumpParam`, never read on PC), Y then X spawn coordinates, and last the destination field ID (`MenuState_opcode_menu_id`). The inline argument is the walkmesh triangle to spawn on (`wm2field_FieldZ`). See [DISC](../11f-disc/) for the disc switch itself. Returns 1.

PC handler: `SCRIPT_DISCJUMP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_DISCJUMP` | 0x521B70 | Field script opcode handler (verified IDA function) |
