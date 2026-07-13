---
layout: default
parent: Field Opcodes
title: 03B_LINEOFF
nav_order: 60
permalink: /technical-reference/field/field-opcodes/03b-lineoff/
---

-   Opcode: **0x03B**
-   Short name: **LINEOFF**
-   Long name: Line Collisions Off

#### Argument

none

#### Stack

  
**LINEOFF**

#### Description

Disables line collisions with this entity by writing 0 to the line's active flag (entity+404). Returns 2 (done + continue).

PC handler: `SCRIPT_LINEOFF` at 0x51DD00.
