---
layout: default
parent: Field Opcodes
title: 02C_BASEANIME
nav_order: 45
permalink: /technical-reference/field/field-opcodes/02c-baseanime/
---

-   Opcode: **0x02C**
-   Short name: **BASEANIME**
-   Long name: Set base animation

#### Argument

Idle animation ID.

#### Stack

  
*Walk animation ID*

*Run animation ID*

**BASEANIME**

#### Description

Registers this entity's three "base" locomotion animation IDs. The inline 8-bit argument becomes `baseanim1` (entity+591, the idle animation restored when movement stops), the top stack value becomes `baseanim2` (entity+592, the walk animation) and the next becomes `baseanim3` (entity+593, the run animation). The [MOVE](../03e-move/) family selects `baseanim2` or `baseanim3` automatically from the entity's move speed, and restores `baseanim1` on arrival. Returns 2 (done + continue).

PC handler: `SCRIPT_BASEANIME` at 0x51D9B0.
