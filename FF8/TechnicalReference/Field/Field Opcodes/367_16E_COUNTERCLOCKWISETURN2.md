---
layout: default
parent: Field Opcodes
title: 16E_COUNTERCLOCKWISETURN2
nav_order: 367
permalink: /technical-reference/field/field-opcodes/16e-counterclockwiseturn2/
---

-   Opcode: **0x16E**
-   Short name: **COUNTERCLOCKWISETURN2**
-   Long name: Counterclockwise Turn

#### Argument

none

#### Stack

  
*Angle*

*Duration of turn (frames)*

**COUNTERCLOCKWISETURN2**

#### Description

Turns this entity to face a target direction, always sweeping in the counter-clockwise sense. Pops the turn **duration** (entity+578) and the **target angle** (entity+478), records the current facing as the start angle (entity+476), and forces the counter-clockwise sweep by adding 256 to the target when the start angle is above it (256 = one full FF8 field turn).

The difference from [COUNTERCLOCKWISETURN](../16c-counterclockwiseturn/) is a **single byte**: this opcode writes turn-mode **2** into entity+580, whereas COUNTERCLOCKWISETURN writes **1** (selecting a different rotation-update path in the per-frame movement tick). Everything else is byte-for-byte identical. Yields until the turn finishes (tick sets entity+580 to 3).

PC handler: `SCRIPT_COUNTERCLOCKWISETURN2`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_COUNTERCLOCKWISETURN2` | 0x5271B0 | Field script opcode handler (verified IDA function) |
