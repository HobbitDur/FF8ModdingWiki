---
layout: default
parent: Field Opcodes
title: 00E_PSHM_L
nav_order: 15
permalink: /technical-reference/field/field-opcodes/00e-pshm-l/
---

-   Opcode: **0x00E**
-   Short name: **PSHM\_L**
-   Long name: Push from memory (long)

#### Argument

Byte offset into the savemap field-variable block (`VARMAP_START`), i.e. a savemap variable number — not a raw pointer.

#### Stack

... =&gt; ..., *value*

#### Description

Push the 32-bit value stored at variable offset **Argument** onto the stack. Returns 2.

PC handler: `SCRIPT_PSHM_L`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_PSHM_L` | 0x51CB70 | Field script opcode handler (verified IDA function) |
