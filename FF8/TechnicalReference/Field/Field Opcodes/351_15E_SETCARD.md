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

Moves a card to the location (Deck ID) **Deck ID**. `I[0]` receives `0` on
success, `-1` on failure.

The script pushes the Deck ID first and the Card ID last, so the handler pops
the Card ID first.

- **Rare card** (ID 77-109): rare cards are unique, the card's location simply
  becomes Deck ID. Deck ID `240` gives it to the player; it does **not** mark
  the card as "ever obtained" (use
  [GETCARD]({{ site.baseurl }}/technical-reference/field/field-opcodes/136-getcard/)
  for that).
- **Normal card** (ID 0-76): normal cards are counted, not located.
  - Deck ID `240`: adds one copy to the player's collection (fails at 100).
    Unlike GETCARD it does not set the card's "owned" flag, so a card the player
    never owned before still reads as not owned (HOWMANYCARD returns `-1`).
  - Any other Deck ID: removes one copy from the player's collection (fails at
    0). The Deck ID value itself is not stored.

See the [CARDGAME Deck ID]({{ site.baseurl }}/technical-reference/field/field-opcodes/13a-cardgame/#deck-id-owner-location)
section for what the locations mean. In the vanilla game SETCARD is used by the
Queen of Cards scripts (`dopub_2`, `eapod1`) and the CC Group scripts
(`bgmon_4`, `rg*` maps).

#### Reference (addresses)

| Function             | Address  | Description                                  |
|----------------------|----------|----------------------------------------------|
| `SCRIPT_SETCARD`     | 0x522500 | Field script opcode handler                  |
| `MoveCardToLocation` | 0x5347F0 | Card move routine, `(card id, location)`     |
