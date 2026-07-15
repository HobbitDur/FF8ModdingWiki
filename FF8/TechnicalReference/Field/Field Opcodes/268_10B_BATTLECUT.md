---
layout: default
parent: Field Opcodes
title: 10B_BATTLECUT
nav_order: 268
permalink: /technical-reference/field/field-opcodes/10b-battlecut/
---

-   Opcode: **0x10B**
-   Short name: **BATTLECUT**
-   Long name: (?)

#### Argument

none

#### Stack

none

#### Description

Disables battles on the current field: the handler sets the savemap `battleOff` flag to 1 and also sets a misc-flag bit (`VAR_MISC_FLAG_UNK6`). While `battleOff` is set, random encounters do not trigger. Takes no stack arguments. It is mostly seen in debug rooms, but the effect is real.

PC handler: `SCRIPT_BATTLECUT`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_BATTLECUT` | 0x523350 | Field script opcode handler (verified IDA function) |
