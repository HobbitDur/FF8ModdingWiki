---
layout: default
parent: Field Opcodes
title: 085_CTURNL
nav_order: 134
permalink: /technical-reference/field/field-opcodes/085-cturnl/
---

-   Opcode: **0x085**
-   Short name: **CTURNL**
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

It's unknown how this is any different from [CTURNR](084_CTURNR).
