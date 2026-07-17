---
layout: default
parent: Field Opcodes
title: 071_DSCROLL
nav_order: 114
permalink: /technical-reference/field/field-opcodes/071-dscroll/
---

-   Opcode: **0x071**
-   Short name: **DSCROLL**
-   Long name: ????

#### Argument

none

#### Stack

  
*Target X*

*Target Y*

**DSCROLL**

#### Description

**D**irect (instant) background scroll. Pops two values (a target X then a target Y) into the scroll-target registers (`word_1CE4790` / `word_1CE4792`) and sets the scroll mode to 3 (direct), clearing the scroll-active byte. The camera/background jumps to the given position with no interpolation, unlike the linear ([LSCROLL](../072-lscroll/)) and smooth ([CSCROLL](../073-cscroll/)) variants. Returns 3 (done + yield).

PC handler: `SCRIPT_DSCROLL`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_DSCROLL` | 0x520C40 | Field script opcode handler (verified IDA function) |
