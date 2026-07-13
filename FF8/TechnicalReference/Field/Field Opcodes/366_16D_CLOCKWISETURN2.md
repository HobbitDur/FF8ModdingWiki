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

Turns this entity clockwise to face some direction. The only noticeable difference between this and the other turn functions is that the turn is always clockwise.

It is unknown how this differs from [CLOCKWISETURN](../16b-clockwiseturn/).

PC handler: `SCRIPT_CLOCKWISETURN2` at 0x527110.
