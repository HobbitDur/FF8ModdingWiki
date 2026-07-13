---
layout: default
parent: Field Opcodes
title: 070_PGETINFO
nav_order: 113
permalink: /technical-reference/field/field-opcodes/070-pgetinfo/
---

-   Opcode: **0x070**
-   Short name: **PGETINFO**
-   Long name: Get Party Member Worldspace Coordinates?

#### Argument

none

#### Stack

  
*Party slot*

**PGETINFO**

#### Description

Pops one value (a party slot 0-2), resolves it to that slot's field entity (via the savemap party-entity map), and reads its position and orientation into this script's temp variables (I registers), the same layout as [GETINFO](../066-getinfo/) but for the chosen party member:

- I[0] = X position (walkmesh units; internal fixed-point >> 12)
- I[1] = Y position
- I[2] = Z position
- I[4] = facing direction (0-255)
- I[5] = orientation value (entity +114)
- I[6] = orientation value (entity +118)

(I[3] is left untouched.) Temp variables can be accessed with `PSHI_L`.

PC handler: `SCRIPT_PGETINFO` at 0x51EEB0.
