---
layout: default
parent: Field Opcodes
title: 0E7_ANIMESPEED
nav_order: 232
permalink: /technical-reference/field/field-opcodes/0e7-animespeed/
---

-   Opcode: **0x0E7**
-   Short name: **ANIMESPEED**
-   Long name: Set animation speed

#### Argument

none

#### Stack

  
*Speed (frames of animation per half second)*

**ANIMESPEED**

#### Description

Sets the speed of this entity's animations. Frame speed of 1 means 2 frames per second. The handler pops one 16-bit value and stores it into the entity's animation-speed field (+520).

PC handler: `SCRIPT_ANIMESPEED` at 0x5264A0.
