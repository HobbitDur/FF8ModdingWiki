---
layout: default
parent: Field Opcodes
title: 066_GETINFO
nav_order: 103
permalink: /technical-reference/field/field-opcodes/066-getinfo/
---

-   Opcode: **0x066**
-   Short name: **GETINFO**
-   Long name: Get Worldspace Coordinates?

#### Argument

none

#### Stack

none

#### Description

Reads this entity's current position and orientation into its temp variables (I registers), all at once:

- I[0] = X position (walkmesh units; internal fixed-point >> 12)
- I[1] = Y position
- I[2] = Z position
- I[4] = facing direction (+577, 0-255)
- I[5] = orientation value at +506
- I[6] = orientation value at +510

(I[3] is left untouched.) No stack use. Temp variables can be accessed with `PSHI_L`.

PC handler: `SCRIPT_GETINFO` at 0x51EE30.
