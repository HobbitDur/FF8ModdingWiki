---
layout: default
parent: Field Opcodes
title: 130_PHSENABLE
nav_order: 305
permalink: /technical-reference/field/field-opcodes/130-phsenable/
---

-   Opcode: **0x130**
-   Short name: **PHSENABLE**
-   Long name: Set PHS Enabled

#### Argument

none

#### Stack

  
*0=disable, 1=enable*

**PHSENABLE**

#### Description

Enables or disables the PHS (switch) submenu. The handler pops one value and, unless the savemap misc flag `0x200` is set, sets (non-zero) or clears (0) bit 2 of the savemap "can save here" flags — the same bit that gates PHS access.

PC handler: `SCRIPT_PHSENABLE`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_PHSENABLE` | 0x522280 | Field script opcode handler (verified IDA function) |
