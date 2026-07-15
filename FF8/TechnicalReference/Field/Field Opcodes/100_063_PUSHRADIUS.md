---
layout: default
parent: Field Opcodes
title: 063_PUSHRADIUS
nav_order: 100
permalink: /technical-reference/field/field-opcodes/063-pushradius/
---

-   Opcode: **0x063**
-   Short name: **PUSHRADIUS**
-   Long name: Set Push Radius

#### Argument

none

#### Stack

  
*Distance*

**PUSHRADIUS**

#### Description

Pops one value and stores it as this entity's push radius (+502): the distance at which the player triggers this entity's **push** script. Most events have a push radius of 48 when active and a push radius of 1 when inactive.

PC handler: `SCRIPT_PUSHRADIUS`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_PUSHRADIUS` | 0x51EE00 | Field script opcode handler (verified IDA function) |
