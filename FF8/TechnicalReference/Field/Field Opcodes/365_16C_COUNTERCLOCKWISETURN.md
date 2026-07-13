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

Turns this entity counterclockwise to face some direction. The only noticeable difference between this and the other turn functions is that the turn is always counterclockwise.

It is unknown how this differs from [COUNTERCLOCKWISETURN2](../16e-counterclockwiseturn2/).

PC handler: `SCRIPT_COUNTERCLOCKWISETURN` at 0x527070.
