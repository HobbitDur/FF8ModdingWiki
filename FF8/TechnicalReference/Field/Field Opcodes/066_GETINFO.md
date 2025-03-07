---
layout: default
parent: Field Opcodes
title: 066_GETINFO
permalink: /technicalreference/field/field-opcodes/066-getinfo/
---

-   Opcode: **0x066**
-   Short name: **GETINFO**
-   Long name: Get Worldspace Coordinates?

#### Argument

none

#### Stack

none

#### Description

Pushes this entity's X position into temp variable 0, Y position into temp variable 1, (and maybe z? facing?).

Temp variables can be accessed with PSHI\_L.
