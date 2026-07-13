---
layout: default
parent: Field Opcodes
title: 06D_KEYSCAN
nav_order: 110
permalink: /technical-reference/field/field-opcodes/06d-keyscan/
---

-   Opcode: **0x06D**
-   Short name: **KEYSCAN**
-   Long name: Scan for pressed key

#### Argument

none

#### Stack

  
*Key flags*

**KEYSCAN**

#### Key Flags

  
16: Cancel

32: Menu

64: OK/Accept

128: Card game button (I think it's called "switch")

#### Description

Pops one value (a key mask) and writes 1 to temporary variable I[0] (access with `PSHI_L 0`) if any of those keys are currently **held** in the field's live button state (0x1CE48B0), 0 otherwise. The script does not pause while doing this, so you have to run it in a touch or push script, or inside a looping subroutine.

PC handler: `SCRIPT_KEYSCAN` at 0x51DA50.
