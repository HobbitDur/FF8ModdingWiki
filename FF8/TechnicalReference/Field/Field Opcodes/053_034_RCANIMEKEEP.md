---
layout: default
parent: Field Opcodes
title: 034_RCANIMEKEEP
nav_order: 53
permalink: /technical-reference/field/field-opcodes/034-rcanimekeep/
---

-   Opcode: **0x034**
-   Short name: **RCANIMEKEEP**
-   Long name: Resume script, controlled animation, keep last frame

#### Argument

Model Animation ID

#### Stack

  
*Last frame of animation*

*First frame of animation*

**RCANIMEKEEP**

#### Description

Play a frame range of an animation, then freeze the model on the last frame played. The "R" (resume) variant of [CANIMEKEEP](../030-canimekeep/): pops the first frame (top) and last frame, uses keep-last-frame mode (`execution_flags` bit 0x80, entity+352) and returns 3 immediately without waiting. Used to make a character perform "half an animation" and then finish it later in a script.

PC handler: `SCRIPT_RCANIMEKEEP` at 0x5269E0.
