---
layout: default
parent: Field Opcodes
title: 00B_POPM_B
nav_order: 12
permalink: /technical-reference/field/field-opcodes/00b-popm-b/
---

-   Opcode: **0x00B**
-   Short name: **POPM\_B**
-   Long name: Pop to memory (byte)

#### Argument

Byte offset into the savemap field-variable block (`VARMAP_START`), i.e. a savemap variable number — not a raw pointer.

#### Stack

..., *value* =&gt; ...

#### Description

Pop *value* from stack and store its low byte at variable offset **Argument**. Returns 2.

PC handler: `SCRIPT_POPM_B`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_POPM_B` | 0x51CCA0 | Field script opcode handler (verified IDA function) |
