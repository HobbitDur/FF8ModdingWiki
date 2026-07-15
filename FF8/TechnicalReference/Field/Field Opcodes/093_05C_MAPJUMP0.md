---
layout: default
parent: Field Opcodes
title: 05C_MAPJUMP0
nav_order: 93
permalink: /technical-reference/field/field-opcodes/05c-mapjump0/
---

-   Opcode: **0x05C**
-   Short name: **MAPJUMP0** (digit zero; historically misread as MAPJUMPO)
-   Long name: Map jump

#### Argument

none

#### Stack

  
*Field Map ID*

*Walkmesh ID*

**MAPJUMP0**

#### Description

Jump the player to the field with the given ID and starting on the given walkmesh triangle. The walkmesh is almost always 0 because MAPJUMP0 is intended to be used for teleporting the player into a cutscene, and the cutscenes place the characters where they need to be on initialization, so it doesn't matter where they're initially teleported.

PC handler: `SCRIPT_MAPJUMP0`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MAPJUMP0` | 0x521C30 | Field script opcode handler (verified IDA function) |
