---
layout: default
parent: Field Opcodes
title: 00C_PSHM_W
nav_order: 13
permalink: /technical-reference/field/field-opcodes/00c-pshm-w/
---

-   Opcode: **0x00C**
-   Short name: **PSHM\_W**
-   Long name: Push from memory (word)

#### Argument

Byte offset into the savemap field-variable block (`VARMAP_START`), i.e. a savemap variable number — not a raw pointer.

#### Stack

... =&gt; ..., *value*

#### Description

Push the unsigned word stored at variable offset **Argument** onto the stack. Returns 2.

PC handler: `SCRIPT_PSHM_W` at 0x51CB30.
