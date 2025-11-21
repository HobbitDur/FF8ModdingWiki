---
layout: default
parent: Field Opcodes
title: 11D_GETPARTY
nav_order: 286
permalink: /technical-reference/field/field-opcodes/11d-getparty/
---

-   Opcode: **0x11D**
-   Short name: **GETPARTY**
-   Long name: Get characetr in party slot

#### Argument

none

#### Stack

  
*Party Slot*

**GETPARTY**

#### Description

Pushes the ID of the character in the given slot to temporary variable 0. Has weird results when passed a parameter of 3 or greater (so don't do it!).
