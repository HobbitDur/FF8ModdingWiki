---
layout: default
parent: Field Opcodes
title: 00F_POPM_L
nav_order: 16
permalink: /technical-reference/field/field-opcodes/00f-popm-l/
---

-   Opcode: **0x00F**
-   Short name: **POPM\_L**
-   Long name: Pop to memory (long)

#### Argument

Byte offset into the savemap field-variable block (`VARMAP_START`), i.e. a savemap variable number — not a raw pointer.

#### Stack

..., *value* =&gt; ...

#### Description

Pop *value* from stack and store its full 32 bits at variable offset **Argument**. Returns 2.

PC handler: `SCRIPT_POPM_L` at 0x51CD00.
