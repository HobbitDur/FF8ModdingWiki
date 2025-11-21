---
layout: default
parent: Field Opcodes
title: 070_PGETINFO
nav_order: 113
permalink: /technical-reference/field/field-opcodes/070-pgetinfo/
---

-   Opcode: **0x070**
-   Short name: **PGETINFO**
-   Long name: Get Party Member Worldspace Coordinates?

#### Argument

none

#### Stack

  
*Party slot*

**PGETINFO**

#### Description

Pushes the given party member's X position into temp variable 0, Y position into temp variable 1, (and maybe z? facing?).

Temp variables can be accessed with PSHI\_L.
