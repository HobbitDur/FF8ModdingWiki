---
layout: default
parent: Field Opcodes
title: 05B_ISTOUCH
nav_order: 92
permalink: /technical-reference/field/field-opcodes/05b-istouch/
---

-   Opcode: **0x05B**
-   Short name: **ISTOUCH**
-   Long name: Is Touching

#### Argument

none

#### Stack

  
*Actor code* (set by [PSHAC](013_PSHAC)

**ISTOUCH**

#### Description

Pushes 1 into temp variable 0 is the specified actor is within touch range of this entity. 0 Otherwise.
