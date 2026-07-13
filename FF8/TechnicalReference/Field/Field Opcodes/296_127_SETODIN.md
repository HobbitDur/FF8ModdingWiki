---
layout: default
parent: Field Opcodes
title: 127_SETODIN
nav_order: 296
permalink: /technical-reference/field/field-opcodes/127-setodin/
---

-   Opcode: **0x127**
-   Short name: **SETODIN**
-   Long name: Unlock Odin

#### Argument

none

#### Stack

none

#### Description

Unlocks Odin (as if you beat him).

Runtime note: the handler takes no stack arguments and calls the "Odin possessed" setter, which sets bit `0x02` in `SG_ODIN_ANGEL_GILGA_FLAG` (`0x1CFE97A`). During battle init, `ZANTETSUKEN_sub_482DF0` (`0x482E00`) checks this bit and can queue Odin with a `32/255` RNG check if enemies do not block death. See [GF Summon Runtime](../../../battle/gf-summon-runtime/).

PC handler: `SCRIPT_SETODIN` at 0x5231C0.
