---
layout: default
parent: Field Opcodes
title: 15F_HOWMANYCARD
nav_order: 352
permalink: /technical-reference/field/field-opcodes/15f-howmanycard/
---

-   Opcode: **0x15F**
-   Short name: **HOWMANYCARD**
-   Long name: How Many Card

#### Argument

none

#### Stack

Card ID

**HOWMANYCARD**

#### Description

Stores in `I[0]` how many copies of card **Card ID** the player owns.

- **Normal card** (ID 0-76): the number of copies, or `-1` if the card was
  never owned.
- **Rare card** (ID 77-109): `1` if the player holds it (location `240`), `0`
  if someone else holds it, `-1` if it was never obtained.

#### Reference (addresses)

| Function             | Address  | Description                 |
|----------------------|----------|-----------------------------|
| `SCRIPT_HOWMANYCARD` | 0x522540 | Field script opcode handler |
| `GetOwnedCardCount`  | 0x534950 | Count routine               |
