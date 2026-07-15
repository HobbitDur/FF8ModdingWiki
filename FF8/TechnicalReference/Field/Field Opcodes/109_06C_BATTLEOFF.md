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

Runtime note: this sets the temporary field encounter disable flag checked by the field encounter tick. It prevents field random encounters without changing scripted battles started by [BATTLE](../069-battle/). Concretely it sets the savemap `battleOff` flag and clears the pending re-enable bit. No stack use. See [Encounter Trigger Runtime](../../../battle/encounter-trigger-runtime/).

PC handler: `SCRIPT_BATTLEOFF`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_BATTLEOFF` | 0x523330 | Field script opcode handler (verified IDA function) |
