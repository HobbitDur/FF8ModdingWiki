---
layout: default
parent: Field Opcodes
title: 09D_DISPTIMER
nav_order: 158
permalink: /technical-reference/field/field-opcodes/09d-disptimer/
---

-   Opcode: **0x09D**
-   Short name: **DISPTIMER**
-   Long name: Display countdown timer

#### Argument

none

#### Stack

  
*X position*

*Y position*

**DISPTIMER**

#### Description

Display the countdown timer on the screen and start counting it down. The handler pops the Y position first and the X position second, stores them in the savemap timer-position fields, sets the "show timer" flag in the savemap `miscFlag`, applies the on-screen position (`setFieldTimerPosition`) and enables the countdown (`setBattleCountdown(1)`). Returns 2.

PC handler: `SCRIPT_DISPTIMER` at 0x521730.
