---
layout: default
parent: Field Opcodes
title: 062_TALKRADIUS
nav_order: 99
permalink: /technical-reference/field/field-opcodes/062-talkradius/
---

-   Opcode: **0x062**
-   Short name: **TALKRADIUS**
-   Long name: Set Talk Radius

#### Argument

none

#### Stack

  
*Distance*

**TALKRADIUS**

#### Description

Pops one value and stores it as this entity's talk radius (+504): the maximum distance the player can be to fire this entity's **talk** script when pressing OK. Most humanoids have a talk radius of about 200.

PC handler: `SCRIPT_TALKRADIUS`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_TALKRADIUS` | 0x51EDD0 | Field script opcode handler (verified IDA function) |
