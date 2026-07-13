---
layout: default
parent: Field Opcodes
title: 0F7_RUNDISABLE
nav_order: 248
permalink: /technical-reference/field/field-opcodes/0f7-rundisable/
---

-   Opcode: **0x0F7**
-   Short name: **RUNDISABLE**
-   Long name: Disable Running

#### Argument

none

#### Stack

  
**RUNDISABLE**

#### Description

Disables running. Sets the global `RUN_DISABLE` flag to 1. Takes no stack arguments.

PC handler: `SCRIPT_RUNDISABLE` at 0x526170.
