---
layout: default
parent: Field Opcodes
title: 0F6_RUNENABLE
nav_order: 247
permalink: /technical-reference/field/field-opcodes/0f6-runenable/
---

-   Opcode: **0x0F6**
-   Short name: **RUNENABLE**
-   Long name: Enable Running

#### Argument

none

#### Stack

  
**RUNENABLE**

#### Description

Enables running. Clears the global `RUN_DISABLE` flag (sets it to 0). Takes no stack arguments.

PC handler: `SCRIPT_RUNENABLE` at 0x526180.
