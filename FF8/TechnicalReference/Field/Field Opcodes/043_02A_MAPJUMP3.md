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

Facing direction / Z on the destination field (16-bit; stored to `wm2field_FieldZ`).

#### Stack

  
*Destination Field Map ID*

*(extra parameter)*

*YCoord*

*XCoord*

*(entry parameter)*

**MAPJUMP3**

#### Description

Same as [MAPJUMP](../029-mapjump/) but pops one extra value. The five stack values are, from the top: destination field map ID (`wm2field_FieldTarget`), an extra parameter stored to `word_1CE4768`, the Y and X spawn coordinates (`wm2field_FieldY`/`wm2field_FieldX`), and a final value copied to `MenuState_opcode_menu_id`. The inline 16-bit argument is written to `wm2field_FieldZ`. It sets the low byte of `globalFieldNextModuleID` to 1 to request the field change next frame, then returns 1.

The extra `word_1CE4768` value was historically guessed to be a facing angle (never above 360, usually a multiple of 4).

PC handler: `SCRIPT_MAPJUMP3` at 0x521AC0.
