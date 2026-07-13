---
layout: default
parent: Field Opcodes
title: 16B_CLOCKWISETURN
nav_order: 364
permalink: /technical-reference/field/field-opcodes/16b-clockwiseturn/
---

-   Opcode: **0x16B**
-   Short name: **CLOCKWISETURN**
-   Long name: Clockwise Turn

#### Argument

none

#### Stack

  
*Angle*

*Duration of turn (frames)*

**CLOCKWISETURN**

#### Description

Turns this entity to face a target direction, always sweeping in the clockwise sense. The handler pops the turn **duration** (stored at entity+578) and the **target angle** (entity+478), and records the entity's current facing as the start angle (entity+476). To force the clockwise sweep it wraps the target by one full turn when needed: if the start angle is below the target it subtracts 256 (a full FF8 field turn = 256 units), so the interpolation runs the short clockwise way.

The difference from [CLOCKWISETURN2](../16d-clockwiseturn2/) is a **single byte**: this opcode writes turn-mode **1** into entity+580, whereas CLOCKWISETURN2 writes **2** (which selects a different rotation-update path in the per-frame movement tick). The popped arguments, start/target setup and the ±256 direction forcing are otherwise byte-for-byte identical. The opcode yields until the turn finishes (the tick sets entity+580 to 3).

PC handler: `SCRIPT_CLOCKWISETURN` at 0x526FD0.
