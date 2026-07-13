---
layout: default
parent: Field Opcodes
title: 0EE_FCOLSUB
nav_order: 239
permalink: /technical-reference/field/field-opcodes/0ee-fcolsub/
---

-   Opcode: **0x0EE**
-   Short name: **FCOLSUB**
-   Long name: Subtractive screen color fade

#### Argument

none

#### Stack

  
*Red Start*

*Green Start*

*Blue Start*

*Red End*

*Green End*

*Blue End*

*Transition Time*

**FCOLSUB**

#### Description

Runs a full-screen color fade in **subtract** mode. The handler sets the field fade state to 6 (subtractive), then pops seven values (start RGB, end RGB, and the transition duration in frames) into the fade-color registers and mirrors all of them into the savemap fade block so the effect survives across frames. Over *Transition Time* frames the screen color is interpolated from the start RGB to the end RGB and subtracted from the rendered image.

PC handler: `SCRIPT_FCOLSUB` at 0x528B20.
