---
layout: default
parent: Field Opcodes
title: 01C_HALT
nav_order: 29
permalink: /technical-reference/field/field-opcodes/01c-halt/
---

-   Opcode: **0x01C**
-   Short name: **HALT**
-   Long name: Halt

#### Argument

Always 0.

#### Stack

No change.

#### Description

Exits the current script and all scripts that are waiting on it. To end only the current script, use RET instead.
