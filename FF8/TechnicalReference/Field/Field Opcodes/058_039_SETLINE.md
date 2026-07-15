---
layout: default
parent: Field Opcodes
title: 039_SETLINE
nav_order: 58
permalink: /technical-reference/field/field-opcodes/039-setline/
---

-   Opcode: **0x039**
-   Short name: **SETLINE**
-   Long name: Set Line Bounds

#### Argument

none

#### Stack

  
*X1*

*Y1*

*Z1*

*X2*

*Y2*

*Z2*

**SETLINE**

#### Description

Sets the bounds of this line object (for its touchOn, touchOff, and across scripts). Lines are actually 3D hitboxes, not lines. The handler pops six 16-bit values — two corner points (X1,Y1,Z1 and X2,Y2,Z2) — into the line's bounds fields (entity+392..+402), then enables the line by writing 1 to its active flag (entity+404) and records the owning script entity index (entity+405). Returns 2 (done + continue).

PC handler: `SCRIPT_SETLINE`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SETLINE` | 0x51DC30 | Field script opcode handler (verified IDA function) |
