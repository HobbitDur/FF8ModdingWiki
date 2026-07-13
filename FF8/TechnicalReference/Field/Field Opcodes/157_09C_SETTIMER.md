---
layout: default
parent: Field Opcodes
title: 09C_SETTIMER
nav_order: 157
permalink: /technical-reference/field/field-opcodes/09c-settimer/
---

-   Opcode: **0x09C**
-   Short name: **SETTIMER**
-   Long name: Set countdown timer time

#### Argument

none

#### Stack

  
*Amount of seconds*

**SETTIMER**

#### Description

Sets the countdown timer's remaining time. The handler pops one word and stores it into the global countdown value (`SG_COUNTDOWN`). This only sets the time; use [DISPTIMER](../09d-disptimer/) to show it and start counting down. Returns 2.

PC handler: `SCRIPT_SETTIMER` at 0x5216E0.
