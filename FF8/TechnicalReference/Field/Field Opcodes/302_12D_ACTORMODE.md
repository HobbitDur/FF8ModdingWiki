---
layout: default
parent: Field Opcodes
title: 12D_ACTORMODE
nav_order: 302
permalink: /technical-reference/field/field-opcodes/12d-actormode/
---

-   Opcode: **0x12D**
-   Short name: **ACTORMODE**
-   Long name: Set Actor Mode

#### Argument

none

#### Stack

  
*Mode*

**ACTORMODE**

#### Description

Controls transparency/blinking effects on models (might also control whether Squall/Seifer's gunblades are visible). The handler pops one *Mode* value and toggles bits in the entity's flag word (+352) plus issues a texture command to the model:

  
0: set the transparency flag (bit 0x2000000), texture command 15

1: clear the transparency flag, texture command 15

2: clear bit 0x1000000, texture command 34

3: set bit 0x1000000, texture command 33

Any other value only issues the texture command.

PC handler: `SCRIPT_ACTORMODE` at 0x51F1F0.
