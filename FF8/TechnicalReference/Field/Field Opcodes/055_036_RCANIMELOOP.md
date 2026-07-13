---
layout: default
parent: Field Opcodes
title: 036_RCANIMELOOP
nav_order: 55
permalink: /technical-reference/field/field-opcodes/036-rcanimeloop/
---

-   Opcode: **0x036**
-   Short name: **RCANIMELOOP**
-   Long name: Resume script, Play controlled looping animation

#### Argument

Model Animation ID

#### Stack

  
*Last frame of animation*

*First frame of animation*

**RCANIMELOOP**

#### Description

Loops a frame range of an animation. The controlled-range variant of [RANIMELOOP](../035-ranimeloop/): pops the first frame (top of stack) and last frame, starts the range in looping mode (`execution_flags` bits set to 0x20, entity+352) and returns 3 immediately, so the range keeps cycling while the script continues.

PC handler: `SCRIPT_RCANIMELOOP` at 0x526AB0.
