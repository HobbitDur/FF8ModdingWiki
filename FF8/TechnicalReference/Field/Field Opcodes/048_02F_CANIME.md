---
layout: default
parent: Field Opcodes
title: 02F_CANIME
nav_order: 48
permalink: /technical-reference/field/field-opcodes/02f-canime/
---

-   Opcode: **0x02F**
-   Short name: **CANIME**
-   Long name: Controlled animation

#### Argument

Model Animation ID

#### Stack

  
*Last frame of animation*

*First frame of animation*

**CANIME**

#### Description

Play a frame range of an animation, then return the model to its base animation. Two values are popped: the first frame (top of stack) and the last frame; internally they are scaled (frame*16 − 16) into the animation frame counters. Uses play-once mode (`execution_flags` bit 0x40, entity+352) and pauses the script until the range finishes.

PC handler: `SCRIPT_CANIME` at 0x5266D0.
