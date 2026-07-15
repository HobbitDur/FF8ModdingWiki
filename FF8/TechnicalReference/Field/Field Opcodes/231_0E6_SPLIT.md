---
layout: default
parent: Field Opcodes
title: 0E6_SPLIT
nav_order: 231
permalink: /technical-reference/field/field-opcodes/0e6-split/
---

-   Opcode: **0x0E6**
-   Short name: **SPLIT**
-   Long name: Split followers

#### Argument

none

#### Stack

  
*X position to send member 2*

*Y position to send member 2*

*Z position to send member 2*

*X position to send member 3*

*Y position to send member 3*

*Z position to send member 3*

*X position to send member 1*

*Y position to send member 1*

*Z position to send member 1*

**SPLIT**

#### Description

Disables the party-member conga line and sends each of the three followers to a specific spot. The handler pops nine values as three X/Y/Z triples; each coordinate is shifted left 12 bits (converted to world fixed-point) before use. It looks up the three current party entities from the savemap party map and walks each one to its target position, setting each entity's "moving" flag. The opcode yields (return 1) every frame until all three followers have arrived, then clears their moving flags and returns.

PC handler: `SCRIPT_SPLIT`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SPLIT` | 0x525090 | Field script opcode handler (verified IDA function) |
