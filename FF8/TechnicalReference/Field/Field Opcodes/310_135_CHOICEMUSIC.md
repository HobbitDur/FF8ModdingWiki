---
layout: default
parent: Field Opcodes
title: 135_CHOICEMUSIC
nav_order: 310
permalink: /technical-reference/field/field-opcodes/135-choicemusic/
---

-   Opcode: **0x135**
-   Short name: **CHOICEMUSIC**
-   Long name: Play the concert music

#### Argument

none

#### Stack

*Music part mask*

**CHOICEMUSIC**

#### Description

Starts the Fisherman's Horizon concert piece with the parts in the mask, once per loaded track, and stores the handle in the savemap music field. Variable 360 holds the mask, built from the four instrument choices in variables 346-349. Only the low 26 bits of the mask are used.

PC handler: `SCRIPT_CHOICEMUSIC`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_CHOICEMUSIC` | 0x51F9A0 | Field script opcode handler (verified IDA function) |
