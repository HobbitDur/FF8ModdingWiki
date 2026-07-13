---
layout: default
parent: Field Opcodes
title: 0AF_SHADELEVEL
nav_order: 176
permalink: /technical-reference/field/field-opcodes/0af-shadelevel/
---

\_\_NOTOC\_\_

-   Opcode: **0x0AF**
-   Short name: **SHADELEVEL**
-   Long name: Shade Level

#### Argument

none

#### Stack

  
*Shade level*

**SHADELEVEL**

#### Description

Sets this actor's shade (lighting) level. The handler pops one byte and stores it in the entity field at `entity+609`, which the model renderer uses to darken/brighten the actor. Returns 2.

PC handler: `SCRIPT_SHADELEVEL` at 0x526E30.
