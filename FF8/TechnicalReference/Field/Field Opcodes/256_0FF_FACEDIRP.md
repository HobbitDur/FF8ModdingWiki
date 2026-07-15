---
layout: default
parent: Field Opcodes
title: 0FF_FACEDIRP
nav_order: 256
permalink: /technical-reference/field/field-opcodes/0ff-facedirp/
---

-   Opcode: **0x0FF**
-   Short name: **FACEDIRP**
-   Long name: Head face to party member

#### Argument

none

#### Stack

  
*Party member ID*

*Frame count*

**FACEDIRP**

#### Description

Turns this actor's head to face the given party member over *frame count*. Identical to [FACEDIRA](../0fe-facedira/) except the target is resolved from the savemap party map (party member ID) rather than a raw actor code.

PC handler: `SCRIPT_FACEDIRP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_FACEDIRP` | 0x527D30 | Field script opcode handler (verified IDA function) |
