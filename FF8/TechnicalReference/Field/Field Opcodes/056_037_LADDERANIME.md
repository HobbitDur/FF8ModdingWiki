---
layout: default
parent: Field Opcodes
title: 037_LADDERANIME
nav_order: 56
permalink: /technical-reference/field/field-opcodes/037-ladderanime/
---

-   Opcode: **0x037**
-   Short name: **LADDERANIME**
-   Long name: Set ladder animations

#### Argument

First ladder animation ID.

#### Stack

  
*Second ladder animation ID*

*Third ladder animation ID*

**LADDERANIME**

#### Description

Registers this entity's three ladder-climb animation IDs, the ladder counterpart of [BASEANIME](../02c-baseanime/). The inline 8-bit argument becomes `ladderanim1` (entity+594), the top stack value becomes `ladderanim2` (entity+595) and the next becomes `ladderanim3` (entity+596). These are the animations used while the entity is on a ladder ([LADDERUP2](../027-ladderup2/) / [LADDERDOWN2](../028-ladderdown2/) modes). Returns 2 (done + continue).

PC handler: `SCRIPT_LADDERANIME` at 0x51DA00.
