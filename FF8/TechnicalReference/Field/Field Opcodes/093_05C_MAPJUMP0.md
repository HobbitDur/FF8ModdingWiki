---
layout: default
parent: Field Opcodes
title: 05C_MAPJUMP0
nav_order: 93
permalink: /technical-reference/field/field-opcodes/05c-mapjump0/
author: HobbitDur
---

-   Opcode: **0x05C**
-   Short name: **MAPJUMP0** (digit zero; historically misread as MAPJUMPO)
-   Long name: Map jump

#### Argument

none

#### Stack

  
*Field Map ID*

*Walkmesh ID*

**MAPJUMP0**

#### Description

Jump the player to the field with the given ID and starting on the given walkmesh triangle. The handler pops the triangle (top of stack, `wm2field_FieldZ`) then the field ID (`MenuState_opcode_menu_id`), sets the facing (`wm2field_FieldTarget`) to 0 and both `wm2field_FieldX` and `wm2field_FieldY` to 0x7FFF, which places the party at the centre of that triangle (`Field_Walkmesh_PlaceEntitiesOnLoad`). The walkmesh is almost always 0 because MAPJUMP0 is intended to be used for teleporting the player into a cutscene, and the cutscenes place the characters where they need to be on initialization, so it doesn't matter where they're initially teleported. Across the retail scripts, 904 of the 1037 uses give triangle 0. The handler only acts on the first frame it runs: the ready-mask test (`ready_bit_index` / `opcode_ready_mask`) lets it pop its values once, and returning 1 never advances the script, so the script stays on this opcode until the field unloads. Nothing placed after it runs.

The field ID is a 0-based line of `maplist`, so values below 102 are valid: see [Field IDs below 102]({{ site.baseurl }}/technical-reference/field/field-jump/#field-ids-below-102). The opcode always asks for the field module, so an ID below 72 does not reach the world map the way a gateway does. For example `MAPJUMP0(76, 0)` goes to `ending` and `MAPJUMP0(95, 0)` to `testbl6`.

PC handler: `SCRIPT_MAPJUMP0`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MAPJUMP0` | 0x521C30 | Field script opcode handler (verified IDA function) |
