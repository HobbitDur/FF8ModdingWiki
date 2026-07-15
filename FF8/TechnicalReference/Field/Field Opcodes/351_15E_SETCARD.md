---
layout: default
parent: Field Opcodes
title: 15E_SETCARD
nav_order: 351
permalink: /technical-reference/field/field-opcodes/15e-setcard/
---

-   Opcode: **0x15E**
-   Short name: **SETCARD**
-   Long name: Set Card

#### Argument

none

#### Stack

  
Deck ID

Card ID

**SETCARD**

#### Description

Moves a card to the specified deck. Sets the first temp variable to 0 if successful.

Rare cards (level 8+) are unique, moving from deck to deck.

If you give the player (deck 240) a non-rare card, it adds one to their collection (max 100). If you give anyone else a non-rare card it *removes* one from the player's collection.

The handler pops two values — Deck ID (top) and Card ID — calls the card-move routine `sub_5347F0(deckID, cardID)`, and stores its return value into temp variable 0 (I[0], entity+320).

PC handler: `SCRIPT_SETCARD`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SETCARD` | 0x522500 | Field script opcode handler (verified IDA function) |
