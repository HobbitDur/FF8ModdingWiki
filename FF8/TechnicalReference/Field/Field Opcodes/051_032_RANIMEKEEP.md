---
layout: default
parent: Field Opcodes
title: 032_RANIMEKEEP
nav_order: 51
permalink: /technical-reference/field/field-opcodes/032-ranimekeep/
---

-   Opcode: **0x032**
-   Short name: **RANIMEKEEP**
-   Long name: Resume script, Animate, keep last frame

#### Argument

Model Animation ID

#### Stack

none

#### Description

Play an animation, then freeze the model on the last frame of the animation. The "R" (resume) variant of [ANIMEKEEP](../02e-animekeep/): keep-last-frame mode (`execution_flags` bit 0x80, entity+352) but returns 3 immediately without waiting, so the script keeps running.

PC handler: `SCRIPT_RANIMEKEEP` at 0x526910.
