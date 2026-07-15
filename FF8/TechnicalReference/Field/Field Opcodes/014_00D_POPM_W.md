---
layout: default
parent: Field Opcodes
title: 00D_POPM_W
nav_order: 14
permalink: /technical-reference/field/field-opcodes/00d-popm-w/
---

-   Opcode: **0x00D**
-   Short name: **POPM\_W**
-   Long name: Pop to memory (word)

#### Argument

Byte offset into the savemap field-variable block (`VARMAP_START`), i.e. a savemap variable number — not a raw pointer.

#### Stack

..., *value* =&gt; ...

#### Description

Pop *value* from stack and store its low word at variable offset **Argument**. Returns 2.

PC handler: `SCRIPT_POPM_W`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_POPM_W` | 0x51CCD0 | Field script opcode handler (verified IDA function) |
