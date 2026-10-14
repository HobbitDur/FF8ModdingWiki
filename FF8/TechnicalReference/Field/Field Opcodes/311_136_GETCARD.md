---
layout: default
parent: Field Opcodes
title: 136_GETCARD
nav_order: 311
permalink: /technical-reference/field/field-opcodes/136-getcard/
---

-   Opcode: **0x136**
-   Short name: **GETCARD**
-   Long name: Get Card

#### Argument

none

#### Stack

Card ID

**GETCARD**

#### Description

Gives card **Card ID** to the player. `I[0]` receives `0` on success, `-1` on
failure.

- **Rare card** (ID 77-109): the card's location becomes the player (`240`) and
  the card is marked as "ever obtained" (the flag the card menu and the
  collection-complete check use).
- **Normal card** (ID 0-76): the card is marked as owned once and one copy is
  added (fails at 100 copies).

#### Reference (addresses)

| Function                    | Address  | Description                 |
|-----------------------------|----------|-----------------------------|
| `SCRIPT_GETCARD`            | 0x5224D0 | Field script opcode handler |
| `AddCardToPlayerCollection` | 0x534840 | Card give routine           |
