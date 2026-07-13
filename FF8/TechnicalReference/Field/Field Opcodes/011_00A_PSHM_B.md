---
layout: default
parent: Field Opcodes
title: 00A_PSHM_B
nav_order: 11
permalink: /technical-reference/field/field-opcodes/00a-pshm-b/
---

-   Opcode: **0x00A**
-   Short name: **PSHM\_B**
-   Long name: Push from memory (byte)

#### Argument

Byte offset into the savemap field-variable block (`VARMAP_START`), i.e. a savemap variable number — not a raw pointer.

#### Stack

... =&gt; ..., *value*

#### Description

Push the unsigned byte stored at variable offset **Argument** onto the stack. Returns 2.

PC handler: `SCRIPT_PSHM_B` at 0x51CAF0.
