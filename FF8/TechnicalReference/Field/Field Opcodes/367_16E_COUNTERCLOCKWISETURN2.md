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

Turns this entity counterclockwise to face some direction. The only noticeable difference between this and the other turn functions is that the turn is always counterclockwise.

It is unknown how this differs from [COUNTERCLOCKWISETURN](../16c-counterclockwiseturn/).

PC handler: `SCRIPT_COUNTERCLOCKWISETURN2` at 0x5271B0.
