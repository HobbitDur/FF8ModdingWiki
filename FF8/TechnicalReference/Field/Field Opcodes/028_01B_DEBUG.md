---
layout: default
parent: Field Opcodes
title: 01B_DEBUG
nav_order: 28
permalink: /technical-reference/field/field-opcodes/01b-debug/
---

-   Opcode: **0x01B**
-   Short name: **DEBUG**
-   Long name: Debug

#### Argument

none

#### Stack

none

#### Description

No gameplay effect in the retail build. The handler sets a global debug flag (`unk_1D9CDC0` = 1) and yields (returns 3); the flag is not read by any shipped code path, so it is a leftover development hook.

PC handler: `SCRIPT_DEBUG`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_DEBUG` | 0x51D700 | Field script opcode handler (verified IDA function) |
