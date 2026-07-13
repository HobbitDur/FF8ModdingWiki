---
layout: default
parent: Field Opcodes
title: 06C_BATTLEOFF
nav_order: 109
permalink: /technical-reference/field/field-opcodes/06c-battleoff/
---

-   Opcode: **0x06C**
-   Short name: **BATTLEOFF**
-   Long name: Battles off

#### Argument

none

#### Stack

none

#### Description

Disables random battles.

Runtime note: this sets the temporary field encounter disable flag checked by the field encounter tick. It prevents field random encounters without changing scripted battles started by [BATTLE](../069-battle/). See [Encounter Trigger Runtime](../../../battle/encounter-trigger-runtime/).
