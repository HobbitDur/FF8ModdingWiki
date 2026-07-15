---
layout: default
parent: Field Opcodes
title: 068_THROUGHOFF
nav_order: 105
permalink: /technical-reference/field/field-opcodes/068-throughoff/
---

-   Opcode: **0x068**
-   Short name: **THROUGHOFF**
-   Long name: Through mode off

#### Argument

none

#### Stack

none

#### Description

Enables collision with this entity by clearing its through flag (+588 = 0), so the player is blocked by it. No stack use.

PC handler: `SCRIPT_THROUGHOFF`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_THROUGHOFF` | 0x51ED60 | Field script opcode handler (verified IDA function) |
