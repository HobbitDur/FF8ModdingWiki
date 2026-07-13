---
layout: default
parent: Field Opcodes
title: 06B_BATTLEON
nav_order: 108
permalink: /technical-reference/field/field-opcodes/06b-battleon/
---

-   Opcode: **0x06B**
-   Short name: **BATTLEON**
-   Long name: Battles on

#### Argument

none

#### Stack

none

#### Description

Enables random battles.

Runtime note: this clears the temporary field encounter disable flag checked by the field encounter tick. Random encounters are still blocked by cutscenes, field state, map encounter settings and Enc-None. Concretely it clears the savemap `battleOff` flag (unless a cutscene lock is active, in which case it just clears the pending disable bit). No stack use. See [Encounter Trigger Runtime](../../../battle/encounter-trigger-runtime/).

PC handler: `SCRIPT_BATTLEON` at 0x523300.
