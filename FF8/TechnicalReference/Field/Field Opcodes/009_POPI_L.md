---
layout: default
parent: Field Opcodes
title: 009_POPI_L
permalink: /technical-reference/field/field-opcodes/009-popi-l/
---

-   Opcode: **0x009**
-   Short name: **POPI\_L**
-   Long name: Pop to Temp List (long)

#### Argument

Index position in the Temp List (0 &lt;= **Argument** &lt; 8).

#### Stack

..., *value* =&gt; ...

#### Description

Pop the top *value* from the stack and store the first four bytes (long) at index position **Argument** in the Temp List.
