---
layout: default
parent: Field Opcodes
title: 01A_UNUSE
nav_order: 27
permalink: /technical-reference/field/field-opcodes/01a-unuse/
---

-   Opcode: **0x01A**
-   Short name: **UNUSE**
-   Long name: Unuse entity

#### Argument

Always 0.

#### Stack

No change.

#### Description

Disable this entity's scripts, hides its model, and makes it throughable. Call [USE](../0e5-use/) to re-enable.

PC handler: `SCRIPT_UNUSE` (unused / no-op opcode).

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_UNUSE` | 0x51DD80 | Field script opcode handler (verified IDA function) |
