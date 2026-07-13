---
layout: default
parent: Field Opcodes
title: 0C3_ALLSEVOL
nav_order: 196
permalink: /technical-reference/field/field-opcodes/0c3-allsevol/
---

-   Opcode: **0x0C3**
-   Short name: **ALLSEVOL**
-   Long name: Set Volume of all Sound Effects

#### Argument

none

#### Stack

  
*Volume (0-127)*

**ALLSEVOL**

#### Description

Sets the volume of all sound-effect channels at once. The handler pops one value (the volume) and applies it to every SE channel immediately (no transition). Returns 2.

PC handler: `SCRIPT_ALLSEVOL` at 0x51FFA0.
