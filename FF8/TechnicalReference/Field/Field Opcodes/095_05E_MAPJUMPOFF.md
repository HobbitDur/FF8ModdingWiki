---
layout: default
parent: Field Opcodes
title: 05E_MAPJUMPOFF
nav_order: 95
permalink: /technical-reference/field/field-opcodes/05e-mapjumpoff/
---

-   Opcode: **0x05E**
-   Short name: **MAPJUMPOFF**
-   Long name: Disable Field Exits

#### Argument

none

#### Stack

  
**MAPJUMPOFF**

#### Description

Prevents the player from leaving the field via a field exit (ie walking off the screen to get to the next area) by setting the field-exit-disable flag (byte at 0x1CE4902 = 1). Undone by [MAPJUMPON](../05d-mapjumpon/). No stack use.

PC handler: `SCRIPT_MAPJUMPOFF` at 0x521CC0.
