---
layout: default
parent: Field Opcodes
title: 029_MAPJUMP
nav_order: 42
permalink: /technical-reference/field/field-opcodes/029-mapjump/
author: HobbitDur
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

Jump the player to another field. The handler pops four values from the stack: the facing direction (top of stack, `wm2field_FieldTarget`), the Y then X spawn coordinates (`wm2field_FieldY`/`wm2field_FieldX`), and last the destination field map ID (`MenuState_opcode_menu_id`, which becomes `CURRENT_FIELD_ID`). The inline 16-bit argument is the walkmesh triangle to spawn on, in the destination field's `.id` (`wm2field_FieldZ`). It then sets the low byte of `globalFieldNextModuleID` to 1, which requests the field module to load the new map next frame. The handler only acts on the first frame it runs: the ready-mask test (`ready_bit_index` / `opcode_ready_mask`) lets it pop its values once, and returning 1 never advances the script, so the script stays on this opcode until the field unloads. Nothing placed after it runs.

The field ID is a 0-based line of `maplist`, so values below 102 are valid: see [Field IDs below 102]({{ site.baseurl }}/technical-reference/field/field-jump/#field-ids-below-102). The opcode always asks for the field module, so an ID below 72 does not reach the world map the way a gateway does.

These are the same globals a walked exit fills from its [gateway record](../../field-file-format/field-gateways/), and the same ones a saved game fills on load (`FFNewGame_or_load`: `SG_COORD_X/Y_PARTY_1`, `SG_TRIANGLE_PARTY_1`, `SG_DIRECTION_PARTY_1`, `SG_CURRENT_FIELD`), which is how their meaning is confirmed.

PC handler: `SCRIPT_MAPJUMP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MAPJUMP` | 0x521A20 | Field script opcode handler (verified IDA function) |
