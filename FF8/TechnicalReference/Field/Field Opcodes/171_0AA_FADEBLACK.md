---
layout: default
parent: Field Opcodes
title: 0AA_FADEBLACK
nav_order: 171
permalink: /technical-reference/field/field-opcodes/0aa-fadeblack/
---

-   Opcode: **0x0AA**
-   Short name: **FADEBLACK**
-   Long name: Fade to black

#### Argument

none

#### Stack

none

#### Description

Fades the screen to black. Takes no arguments and pops nothing; the handler simply sets the field fade state to 4 (both the runtime `FIELD_FADE_STATE` and the savemap copy) and returns 2. The fade itself is carried out by the field fade system.

PC handler: `SCRIPT_FADEBLACK`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_FADEBLACK` | 0x528D10 | Field script opcode handler (verified IDA function) |
