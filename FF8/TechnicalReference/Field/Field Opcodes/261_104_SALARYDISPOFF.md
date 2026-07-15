---
layout: default
parent: Field Opcodes
title: 104_SALARYDISPOFF
nav_order: 261
permalink: /technical-reference/field/field-opcodes/104-salarydispoff/
---

-   Opcode: **0x104**
-   Short name: **SALARYDISPOFF** (exe symbol; historically misspelled SARALYDISPOFF)
-   Long name: Salary display off

#### Argument

none

#### Stack

none

#### Description

Turns off the display of salary alerts.

PC handler: `SCRIPT_SALARYDISPOFF`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SALARYDISPOFF` | 0x51DBF0 | Field script opcode handler (verified IDA function) |
