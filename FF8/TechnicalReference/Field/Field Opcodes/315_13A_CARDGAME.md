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

Game rules (Byte)

Trade rules (Byte)

Rare card chance (Long)

Unknown1 (Long)

Unknown2 (Long)

Allowed card level mask (Long)

**CARDGAME**

#### Description

Starts a game of Triple Triad against the specified deck.
There should be a copy of the "cardgamemaster" entity on the scene to handle all this - call "\[region\]\_maeshori0" before the game, then pass byte vars 292 and 293 into this, and finally call "\[region\]\_shori0" afterwards.

[*Game rules*]({site.baseurl}}/technical-reference/list/card-list#game-rules) are the rules to play the game.

[*Trade rules*]({site.baseurl}}/technical-reference/list/card-list#trade-rules) are the rules to trade the cards.

*Rare card chance*: Each rare card currently held at the challenge's location has a RARE_CARD_CHANCE / 100 probability of being added to the NPC's deck (up to 5 rares). The chance is halved after every successful pick, so additional rares in the same hand become progressively less likely.

*Allowed card level mask*: is a 7 bit mask that define what card level the player can use to pick cards. For example, with 0xA, he can pick either on level 1 or level 3.
