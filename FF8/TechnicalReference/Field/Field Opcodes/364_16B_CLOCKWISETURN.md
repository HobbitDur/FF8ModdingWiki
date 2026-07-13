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

Turns this entity clockwise to face some direction. The only noticeable difference between this and the other turn functions is that the turn is always clockwise.

It is unknown how this differs from [CLOCKWISETURN2](../16d-clockwiseturn2/).

PC handler: `SCRIPT_CLOCKWISETURN` at 0x526FD0.
