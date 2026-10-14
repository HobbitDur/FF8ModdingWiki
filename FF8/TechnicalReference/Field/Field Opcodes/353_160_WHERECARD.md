---
layout: default
parent: Field Opcodes
title: 160_WHERECARD
nav_order: 353
permalink: /technical-reference/field/field-opcodes/160-wherecard/
---

-   Opcode: **0x160**
-   Short name: **WHERECARD**
-   Long name: Where Card

#### Argument

none

#### Stack

Card ID

**WHERECARD**

#### Description

Stores in `I[0]` the current location (Deck ID) of rare card **Card ID**:
`240` for the player, otherwise the Deck ID of the NPC holding it (see the
[CARDGAME Deck ID]({{ site.baseurl }}/technical-reference/field/field-opcodes/13a-cardgame/#deck-id-owner-location)
section). For a normal card (ID 0-76) it returns `0`.

The Queen of Cards and CC Group scripts use it to know who holds each rare card.

#### Reference (addresses)

| Function              | Address  | Description                 |
|-----------------------|----------|-----------------------------|
| `SCRIPT_WHERECARD`    | 0x522570 | Field script opcode handler |
| `GetRareCardLocation` | 0x534A20 | Location read routine       |
