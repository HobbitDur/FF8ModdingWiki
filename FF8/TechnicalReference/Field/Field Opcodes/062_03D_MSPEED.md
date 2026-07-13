---
layout: default
parent: Field Opcodes
title: 03D_MSPEED
nav_order: 62
permalink: /technical-reference/field/field-opcodes/03d-mspeed/
---

-   Opcode: **0x03D**
-   Short name: **MSPEED**
-   Long name: Set Move Speed

#### Argument

none

#### Stack

  
*Speed (units per second?)*

**MSPEED**

#### Description

Sets this entity's movement speed. Pops one 16-bit value and stores it into both the active move-speed field (`move_speed`, entity+510) and its companion slot (entity+512, the value the [MOVE](../03e-move/) family copies back into `move_speed` and compares against a threshold to choose the walk vs. run animation). Returns 2 (done + continue).

PC handler: `SCRIPT_MSPEED` at 0x5233E0.
