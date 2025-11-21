---
layout: default
parent: Field Opcodes
title: 084_CTURNR
nav_order: 133
permalink: /technical-reference/field/field-opcodes/084-cturnr/
---

-   Opcode: **0x084**
-   Short name: **CTURNR**
-   Long name: Turn Character

#### Argument

none

#### Stack

  
*Angle to face*

*Duration of turn* (frames)

**CTURNL**

#### Description

Turns this entity.

Note that Final Fantasy 8 uses 256 degree circles. Degrees 0 and 256 are defined as down, 64 right, 128 up, 192 left.

It's unknown how this is any different from [CTURNL](085_CTURNL).
