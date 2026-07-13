---
layout: default
parent: Field Opcodes
title: 16C_COUNTERCLOCKWISETURN
nav_order: 365
permalink: /technical-reference/field/field-opcodes/16c-counterclockwiseturn/
---

-   Opcode: **0x16C**
-   Short name: **COUNTERCLOCKWISETURN**
-   Long name: Counterclockwise Turn

#### Argument

none

#### Stack

  
*Angle*

*Duration of turn (frames)*

**COUNTERCLOCKWISETURN**

#### Description

Turns this entity to face a target direction, always sweeping in the counter-clockwise sense. Pops the turn **duration** (entity+578) and the **target angle** (entity+478), records the current facing as the start angle (entity+476), and forces the counter-clockwise sweep by adding 256 to the target when the start angle is above it (256 = one full FF8 field turn). This is the mirror of [CLOCKWISETURN](../16b-clockwiseturn/) (which uses the `<` / −256 test instead).

The difference from [COUNTERCLOCKWISETURN2](../16e-counterclockwiseturn2/) is a **single byte**: this opcode writes turn-mode **1** into entity+580, whereas COUNTERCLOCKWISETURN2 writes **2** (selecting a different rotation-update path in the per-frame movement tick). The rest is byte-for-byte identical. Yields until the turn finishes (tick sets entity+580 to 3).

PC handler: `SCRIPT_COUNTERCLOCKWISETURN` at 0x527070.
