---
layout: default
parent: Field Opcodes
title: 04B_WINSIZE
nav_order: 76
permalink: /technical-reference/field/field-opcodes/04b-winsize/
---

-   Opcode: **0x04B**
-   Short name: **WINSIZE**
-   Long name: Set Window Size

#### Argument

none

#### Stack

  
*Message Channel*

*X*

*Y*

*Width*

*Height*

**WINSIZE**

#### Description

Pops five values (message channel, X, Y, Width, Height) and sets the window rectangle for that channel, then calls `setTextPosition`. The rectangle is clamped to the screen: X is pulled in so `X+Width < 304` and never below 8; Y so `Y+Height < 224` and never below 8 (limits of 312x224). The chosen center/size is cached in the per-channel window arrays (`word_1D9CF98`+), so a following MES on the same channel uses it. If the channel is already busy (its bit in `VAR_MAP unk[1]`) the opcode retries (returns 5) without popping.

Only useful before calling MES, which has no built-in size parameters. WINSIZE is only used in the first hallway of the game, where Quistis is imitating Squall (and also in some debug areas). Probably, Square's eventers used this a few times, hated how tedious it was, and asked for the AMES family of opcodes to be added, but didn't change the ones they already did.

PC handler: `SCRIPT_WINSIZE` at 0x529A20.
