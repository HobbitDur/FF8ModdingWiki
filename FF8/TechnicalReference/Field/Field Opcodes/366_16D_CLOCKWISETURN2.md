---
layout: default
parent: Field Opcodes
title: 16D_CLOCKWISETURN2
nav_order: 366
permalink: /technical-reference/field/field-opcodes/16d-clockwiseturn2/
---

-   Opcode: **0x16D**
-   Short name: **CLOCKWISETURN2**
-   Long name: Clockwise Turn

#### Argument

none

#### Stack

  
*Angle*

*Duration of turn (frames)*

**CLOCKWISETURN2**

#### Description

Turns this entity to face a target direction, always sweeping in the clockwise sense. Pops the turn **duration** (entity+578) and the **target angle** (entity+478), records the current facing as the start angle (entity+476), and forces the clockwise sweep by subtracting 256 from the target when the start angle is below it (256 = one full FF8 field turn).

The difference from [CLOCKWISETURN](../16b-clockwiseturn/) is a **single byte**: this opcode writes turn-mode **2** into entity+580, whereas CLOCKWISETURN writes **1** (selecting a different rotation-update path in the per-frame movement tick). Everything else — the popped arguments, start/target setup and the ±256 direction forcing — is byte-for-byte identical. Yields until the turn finishes (tick sets entity+580 to 3).

PC handler: `SCRIPT_CLOCKWISETURN2` at 0x527110.
