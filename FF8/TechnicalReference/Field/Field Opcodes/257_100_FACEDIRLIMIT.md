---
layout: default
parent: Field Opcodes
title: 100_FACEDIRLIMIT
nav_order: 257
permalink: /technical-reference/field/field-opcodes/100-facedirlimit/
---

-   Opcode: **0x100**
-   Short name: **FACEDIRLIMIT**
-   Long name: Limit Head Facing

#### Argument

none

#### Stack

  
*Angle 1?*

*Angle 2?*

*Angle 3?*

**FACEDIRLIMIT**

#### Description

Limits how far this actor's head can turn to face an actor (so they don't go into exorcist mode). The handler pops three bytes and stores them into the entity's head-limit fields at +568, +569 and +570 (in stack push order).

PC handler: `SCRIPT_FACEDIRLIMIT`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_FACEDIRLIMIT` | 0x528300 | Field script opcode handler (verified IDA function) |
