---
layout: default
parent: Field Opcodes
title: 13A_CARDGAME
nav_order: 315
permalink: /technical-reference/field/field-opcodes/13a-cardgame/
---

-   Opcode: **0x13A**
-   Short name: **CARDGAME**
-   Long name: Card Game

#### Argument

none

#### Stack

  
Deck ID (Long)

Known rules (Byte)

Region rules (Byte)

Rare card chance (Long)

Unknown1 (Long)

Unknown2 (Long)

Allowed card level mask (Long)

**CARDGAME**

#### Description

Starts a game of Triple Triad against the specified deck.

"Region rules" are the rules for the region you're in, and "known rules" are the ones you're spreading from elsewhere. There should be a copy of the "cardgamemaster" entity on the scene to handle all this - call "\[region\]\_maeshori0" before the game, then pass byte vars 292 and 293 into this, and finally call "\[region\]\_shori0" afterwards.

"Rare card chance" is a percentage chance (0-100) that the opponent will play a rare card if they have one.

"Allowed card level mask" is a 7 bit mask that define what card level the player can use to pick cards. For example, with 0xA, he can pick either on level 1 or level 3.

Not known what the remaining 3 numbers do yet. Presumably the range of common cards they'll use is included. Maybe some AI characteristics like thinking time.

