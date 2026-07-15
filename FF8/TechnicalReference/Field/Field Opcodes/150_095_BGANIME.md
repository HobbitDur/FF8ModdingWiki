---
layout: default
parent: Field Opcodes
title: 095_BGANIME
nav_order: 150
permalink: /technical-reference/field/field-opcodes/095-bganime/
---

-   Opcode: **0x095**
-   Short name: **BGANIME**
-   Long name: Animate Background

#### Argument

none

#### Stack

  
*Start frame*

*End frame*

**BGANIME**

#### Description

Animates a background object (an animated background layer) on the field between two frames. The handler pops two values: the end frame (top of stack) and the start frame (below it). It stores the range in the background object's animation fields (each frame scaled ×64, the end frame padded with +63 to cover its 64-step block) and sets the "animating" flag. If the end frame is lower than the start frame it plays the range in reverse (sets the reverse-direction flag). It returns 1 (wait) while the animation is running and 2 once it finishes.

PC handler: `SCRIPT_BGANIME`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_BGANIME` | 0x520570 | Field script opcode handler (verified IDA function) |
