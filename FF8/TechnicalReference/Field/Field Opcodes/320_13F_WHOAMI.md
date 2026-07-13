---
layout: default
parent: Field Opcodes
title: 13F_WHOAMI
nav_order: 320
permalink: /technical-reference/field/field-opcodes/13f-whoami/
---

-   Opcode: **0x13F**
-   Short name: **WHOAMI**
-   Long name: Get Junction Correspondent?

#### Argument

none

#### Stack

  
*Character ID*

**WHOAMI**

#### Description

Pops one value (a field character ID), maps it through `getPointerCharaData`, and stores the resulting real-character slot into temp variable 0 (I[0], entity+320).

This is only used twice in the game - both at Esthar's "front gate" before the last dream sequence.

PC handler: `SCRIPT_WHOAMI` at 0x51EF70.
