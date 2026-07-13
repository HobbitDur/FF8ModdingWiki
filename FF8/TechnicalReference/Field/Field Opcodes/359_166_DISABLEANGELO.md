---
layout: default
parent: Field Opcodes
title: 166_DISABLEANGELO
nav_order: 359
permalink: /technical-reference/field/field-opcodes/166-disableangelo/
---

-   Opcode: **0x166**
-   Short name: **DISABLEANGELO**
-   Long name: Disable angelo

#### Argument

none

#### Stack

  
*0 or 1*

**DISABLEANGELO**

#### Description

It uses 1 at the Esthar concourse and the Ragnarok airlock. Uses 0 in the ragnarok cockpit.

Runtime note: controls bit `0x10` in `SG_ODIN_ANGEL_GILGA_FLAG` (`0x1CFE97A`). Angelo auto-actions require Rinoa in the party and this bit clear. See [GF Summon Runtime](../../../battle/gf-summon-runtime/).
