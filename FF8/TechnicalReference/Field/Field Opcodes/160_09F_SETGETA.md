---
layout: default
parent: Field Opcodes
title: 09F_SETGETA
nav_order: 160
permalink: /technical-reference/field/field-opcodes/09f-setgeta/
---

-   Opcode: **0x09F**
-   Short name: **SETGETA**
-   Long name: Set/Get Actor?

#### Argument

none

#### Stack

  
*Height offset ("geta")*

**SETGETA**

#### Description

Sets a per-actor vertical/height offset for this entity's model ("geta", Japanese for raised clog/elevation). The handler pops one byte and stores it in the entity field at `entity+599`; unless a global suppression bit is set (`dword_1D9CDDC & 2`) it also copies the value into the actor's model instance (`+97`), which applies the elevation to the rendered model. Because the value keys off the model, it is the same for a given character in a given field. Returns 2.

PC handler: `SCRIPT_SETGETA`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SETGETA` | 0x526C30 | Field script opcode handler (verified IDA function) |
