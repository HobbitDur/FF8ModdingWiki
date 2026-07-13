---
layout: default
parent: Field Opcodes
title: 109_JUNCTION
nav_order: 266
permalink: /technical-reference/field/field-opcodes/109-junction/
---

-   Opcode: **0x0109**
-   Short name: **JUNCTION**
-   Long name: Set "dream world" status

#### Argument

none

#### Stack

  
*Junction mode*

**JUNCTION**

#### Description

  
When set to 0, ends all "dream world" related stuff (GF junction carryover, Squall-&gt;Laguna, party lock, etc).

When set to 1, only Squall's junctions gets carried over.

When set to 3, the whole party gets carried over.

Runtime: the handler pops one value and calls the Laguna dream-mode setter with bit 0. When bit 0 is set it backs up/carries over the junction data (GFs, junctions) into the reserved savemap region; if bit 1 is also set (value 3) it additionally requests the junction-setup menu (module 5, menu id 22) before yielding. When bit 0 is clear (value 0) it restores the pre-dream junction data instead. Returns 3 (yield).

PC handler: `SCRIPT_JUNCTION` at 0x51EFB0.
