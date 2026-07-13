---
layout: default
parent: Field Opcodes
title: 08B_ISPARTY
nav_order: 140
permalink: /technical-reference/field/field-opcodes/08b-isparty/
---

-   Opcode: **0x08B**
-   Short name: **ISPARTY**
-   Long name: Get position in party

#### Argument

none

#### Stack

  
*Character ID*

**ISPARTY**

#### Description

Pops one word (the character id) and writes that character's slot index in the active party (0, 1 or 2) into I register 0 (`entity+320`, script temporary variable 0). If the character is not in the active party it writes -1. Returns 2.

PC handler: `SCRIPT_ISPARTY` at 0x51E5E0.
