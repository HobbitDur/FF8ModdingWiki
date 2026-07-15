---
layout: default
parent: Field Opcodes
title: 0FE_FACEDIRA
nav_order: 255
permalink: /technical-reference/field/field-opcodes/0fe-facedira/
---

-   Opcode: **0x0FE**
-   Short name: **FACEDIRA**
-   Long name: Head Face towards Actor

#### Argument

none

#### Stack

  
*Actor code (use PSHAC)*

*Frame count*

**FACEDIRA**

#### Description

Turns this actor's head to face the given actor over the duration of *frame count*. The handler pops the frame count and the target actor's script id, queries the target model's world position through the camera, stores it as the head-look target, and enters head-track mode. It yields until the interpolation reaches the requested frame count.

PC handler: `SCRIPT_FACEDIRA`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_FACEDIRA` | 0x527C30 | Field script opcode handler (verified IDA function) |
