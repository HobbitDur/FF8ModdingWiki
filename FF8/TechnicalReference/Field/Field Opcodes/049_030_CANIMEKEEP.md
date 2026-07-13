---
layout: default
parent: Field Opcodes
title: 030_CANIMEKEEP
nav_order: 49
permalink: /technical-reference/field/field-opcodes/030-canimekeep/
---

-   Opcode: **0x030**
-   Short name: **CANIMEKEEP**
-   Long name: Controlled animation, keep last frame

#### Argument

Model Animation ID

#### Stack

  
*Last frame of animation*

*First frame of animation*

**CANIMEKEEP**

#### Description

Play a frame range of an animation, then freeze the model on the last frame played. Same as [CANIME](../02f-canime/) but with the "keep last frame" animation mode (`execution_flags` bit 0x80, entity+352). Two values are popped (first frame on top, then last frame). Pauses the script until the range finishes. Used to make a character perform "half an animation" and then finish it later in a script.

PC handler: `SCRIPT_CANIMEKEEP` at 0x526810.
