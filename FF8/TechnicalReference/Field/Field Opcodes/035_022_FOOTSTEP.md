---
layout: default
parent: Field Opcodes
title: 022_FOOTSTEP
nav_order: 35
permalink: /technical-reference/field/field-opcodes/022-footstep/
---

-   Opcode: **0x022**
-   Short name: **FOOTSTEP**
-   Long name: Set footstep sound mapping

#### Argument

Footstep sound-set id (inline byte).

#### Stack

  
*Key*

**FOOTSTEP**

#### Description

Configures this entity's footstep sound. One value (*Key*) is popped from the stack and stored together with the inline **Argument** into the entity's footstep-config field at +188: byte +188 = *Key* (the surface/region selector), byte +189 = **Argument** (the footstep sound-set id to play on that surface). This is why the game always emits it as a *Key*-*Argument* pair (0-0, 0-1, 1-0, 1-2, 2-3, 3-4, 4-5, 5-6, 6-7, 8-9, 10-11). Returns 2.

PC handler: `SCRIPT_FOOTSTEP` at 0x520460.
