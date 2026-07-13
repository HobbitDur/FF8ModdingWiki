---
layout: default
parent: Field Opcodes
title: 05A_PUSHOFF
nav_order: 91
permalink: /technical-reference/field/field-opcodes/05a-pushoff/
---

-   Opcode: **0x05A**
-   Short name: **PUSHOFF**
-   Long name: Push script off

#### Argument

none

#### Stack

none

#### Description

Disables this entity's "push" script by setting its push-disabled flag (+585 = 1). No stack use. See [PUSHON](../059-pushon/).

PC handler: `SCRIPT_PUSHOFF` at 0x51EC10.
