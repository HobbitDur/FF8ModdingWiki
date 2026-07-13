---
layout: default
parent: Field Opcodes
title: 06E_KEYON
nav_order: 111
permalink: /technical-reference/field/field-opcodes/06e-keyon/
---

-   Opcode: **0x06E**
-   Short name: **KEYON**
-   Long name: Enable Key

#### Argument

none

#### Stack

  
*Key Flags*

**KEYON**

#### Description

Pops one value (a key mask) and writes 1 to temporary variable I[0] (access with `PSHI_L 0`) if any of those keys are set in the secondary button-state register (0x1CE48B8) — the "just pressed / trigger" (edge) state, as opposed to the held state tested by [KEYSCAN](../06d-keyscan/). Writes 0 otherwise. Despite the "Enable Key" long name, the handler is a key-state test, not a key-enable: it neither pops nor changes any enable flag beyond consuming the mask. Non-blocking, like KEYSCAN.

PC handler: `SCRIPT_KEYON` at 0x51DAA0.
