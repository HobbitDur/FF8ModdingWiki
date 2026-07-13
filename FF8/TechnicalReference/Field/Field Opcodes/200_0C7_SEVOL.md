---
layout: default
parent: Field Opcodes
title: 0C7_SEVOL
nav_order: 200
permalink: /technical-reference/field/field-opcodes/0c7-sevol/
---

-   Opcode: **0x0C7;**
-   Short name: **SEVOL**
-   Long name: Set Sound Effect Volume

#### Argument

none

#### Stack

  
*Sound channel*

*Volume (0-127)*

**SEVOL**

#### Description

Sets the volume of a single sound-effect channel. The handler pops the volume first (top of stack) and the channel second, then applies the volume to that channel immediately (`Sfx_SetVolume_Mask`, no transition). Returns 2.

PC handler: `SCRIPT_SEVOL` at 0x520080.
