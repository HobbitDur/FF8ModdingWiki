---
layout: default
parent: Field Opcodes
title: 06A_BATTLERESULT
nav_order: 107
permalink: /technical-reference/field/field-opcodes/06a-battleresult/
---

-   Opcode: **0x06A**
-   Short name: **BATTLERESULT**
-   Long name: Get Battle Result

#### Argument

none

#### Stack

none

#### Description

Writes the outcome byte of the most recent battle (`battle_result_byte` at 0x1CFF6E7) into temp variable I[0] (+320). Read it with `PSHI_L 0`. No stack use.

PC handler: `SCRIPT_BATTLERESULT` at 0x5232E0.
