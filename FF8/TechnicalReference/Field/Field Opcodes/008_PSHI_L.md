---
layout: default
parent: Field Opcodes
title: 008_PSHI_L
nav_order: 9
permalink: /technical-reference/field/field-opcodes/008-pshi-l/
---

-   Opcode: **0x008**
-   Short name: **PSHI\_L**
-   Long name: Push from Temp List (long)

#### Argument

Index position in the Temp List (0 &lt;= **Argument** &lt; 8).

#### Stack

... =&gt; ..., *value*

#### Description

Push the *value* (long) at index position **Argument** in the Temp List onto the stack.
