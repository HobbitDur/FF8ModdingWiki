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

Play the range of frames of an animation, then freeze the model on the last frame played. Pauses script until animation finishes. Used to make a character perform "half an animation" and then finish the animation later in a script.
