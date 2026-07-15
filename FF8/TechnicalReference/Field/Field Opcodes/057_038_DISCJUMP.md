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

Walkmesh ID

#### Stack

  
*Field Map ID*

*XCoord*

*YCoord*

*ZCoord*

*(angle?)*

**DISCJUMP**

#### Description

Same as [MAPJUMP3](../02a-mapjump3/), but requests a disc-change flow instead of a plain field load: it sets the low byte of `globalFieldNextModuleID` to 6 (rather than 1) and raises the `menu_disabled` flag. It pops the same five stack values — destination field ID (`wm2field_FieldTarget`), an extra parameter (`word_1CE4768`), Y and X spawn coordinates, and a final value (`MenuState_opcode_menu_id`) — and writes the inline argument to `wm2field_FieldZ`. See [DISC](../11f-disc/) for the disc switch itself. Returns 1.

PC handler: `SCRIPT_DISCJUMP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_DISCJUMP` | 0x521B70 | Field script opcode handler (verified IDA function) |
