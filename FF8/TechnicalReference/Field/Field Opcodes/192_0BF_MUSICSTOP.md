---
layout: default
parent: Field Opcodes
title: 0BF_MUSICSTOP
nav_order: 192
permalink: /technical-reference/field/field-opcodes/0bf-musicstop/
---

-   Opcode: **0x0BF**
-   Short name: **MUSICSTOP**
-   Long name: Stop Music

#### Argument

none

#### Stack

  
*0 or 1*

**MUSICSTOP**

#### Description

Stops one of the two field music channels. The handler pops one value and masks it to bit 0, giving a channel slot of 0 or 1 (FF8 keeps two music handles for effects like CROSSMUSIC / DUALMUSIC). If that slot currently holds a playing track it stops it and marks the handle unused (-1). Returns 2.

This is why MUSICSTOP is sometimes called twice in a row (once for each slot):

  
PSHN\_L 1

MUSICSTOP

PSHN\_L 0

MUSICSTOP

PC handler: `SCRIPT_MUSICSTOP` at 0x51FBD0.
