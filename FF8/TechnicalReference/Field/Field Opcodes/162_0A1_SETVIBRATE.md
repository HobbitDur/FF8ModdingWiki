---
layout: default
parent: Field Opcodes
title: 0A1_SETVIBRATE
nav_order: 162
permalink: /technical-reference/field/field-opcodes/0a1-setvibrate/
---

-   Opcode: **0x0A1**
-   Short name: **SETVIBRATE**
-   Long name: Vibrate

#### Argument

none

#### Stack

  
*Vibration parameter 1*

*Vibration parameter 2 (flags)*

**SETVIBRATE**

#### Description

Starts a controller vibration (rumble) effect. The handler pops two values and registers a vibration entry from the vibration pattern table (`unk_B8DCB0`) using the first-pushed value as one parameter and the second-pushed value (forced to have bit 0 set, `| 1`) as the other; the returned effect handle is kept in a global (`unk_1D9CDE8`). Returns 2.

PC handler: `SCRIPT_SETVIBRATE` at 0x51F620.
