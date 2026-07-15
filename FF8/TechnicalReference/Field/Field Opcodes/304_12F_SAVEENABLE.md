---
layout: default
parent: Field Opcodes
title: 12F_SAVEENABLE
nav_order: 304
permalink: /technical-reference/field/field-opcodes/12f-saveenable/
---

-   Opcode: **0x12F**
-   Short name: **SAVEENABLE**
-   Long name: Set Save Enabled

#### Argument

none

#### Stack

  
*(0=disable, 1=enable)*

**SAVEENABLE**

#### Description

Enables or disables saving. The handler pops one value and sets (non-zero) or clears (0) the "can save here" bit in the savemap flags.

PC handler: `SCRIPT_SAVEENABLE`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SAVEENABLE` | 0x5221B0 | Field script opcode handler (verified IDA function) |
