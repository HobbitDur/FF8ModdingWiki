---
layout: default
parent: Field Opcodes
title: 126_SETWITCH
nav_order: 295
permalink: /technical-reference/field/field-opcodes/126-setwitch/
---

-   Opcode: **0x0126**
-   Short name: **SETWITCH**
-   Long name: Set Rinoa as Sorceress

#### Argument

none

#### Stack

  
*1*

**SETWITCH**

#### Description

This is only called once in the whole game - the first time you enter the Ragnarok in space. It unlocks Rinoa's alternate limit break after she becomes a sorceress.

Runtime note: sets bit `0x20` in `SG_ODIN_ANGEL_GILGA_FLAG` (`0x1CFE97A`). The same byte also stores Odin, Phoenix, Gilgamesh and Angelo-related battle flags. See [GF Summon Runtime](../../battle/gf-summon-runtime/).
