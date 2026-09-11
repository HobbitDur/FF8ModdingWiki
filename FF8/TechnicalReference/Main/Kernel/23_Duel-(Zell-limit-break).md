---
layout: default
title: Duel (zell limit break)
nav_order: 25
parent: Kernel
permalink: /technical-reference/main/kernel/duel-zell-limit-break/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x48B8 | 10       | 32 bytes     |

## Sections

| Offset | Ability         |
|--------|-----------------|
| 0x48B8 | Punch Rush      |
| 0x48D8 | Booya           |
| 0x48F8 | Heel Drop       |
| 0x4918 | Mach Kick       |
| 0x4938 | Dolphin Blow    |
| 0x4958 | Meteor Strike   |
| 0x4978 | Burning Rave    |
| 0x4998 | Meteor Barret   |
| 0x49B8 | Different Beat  |
| 0x49D8 | My Final Heaven |

## Section Structure

| Offset | Length  | Description                 |
|--------|---------|-----------------------------|
| 0x0000 | 2 bytes | Offset to limit name        |
| 0x0002 | 2 bytes | Offset to limit description |
| 0x0004 | 2 bytes | Magic ID                    |
| 0x0006 | 1 byte  | Attack type                 |
| 0x0007 | 1 byte  | Attack power                |
| 0x0008 | 1 byte  | Target hit animation — the hit/impact animation byte. Duel swaps the flags/animation byte order vs. Magic/Enemy-attack layouts (`Battle_applyDamage`) |
| 0x0009 | 1 byte  | Padding (unused; IDA: 0 xrefs) |
| 0x000A | 1 byte  | Target Info                 |
| 0x000B | 1 bytes | Attack flags — behavior bitfield (low 2 bits also stored as the last-attacker `ATTACK_FLAG`) |
| 0x000C | 1 byte  | Hit count                   |
| 0x000D | 1 byte  | Element Attack              |
| 0x000E | 1 byte  | Element Attack %            |
| 0x000F | 1 byte  | Status attack accuracy       |
| 0x0010 | 2 bytes | [Sequence Button 1](#sequence-buttons) — also carries the [finisher flag](#the-finisher-flag-bit-0x0100-of-button-1) in bit 0x0100 |
| 0x0012 | 2 bytes | Sequence Button 2           |
| 0x0014 | 2 bytes | Sequence Button 3           |
| 0x0016 | 2 bytes | Sequence Button 4           |
| 0x0018 | 2 bytes | Sequence Button 5           |
| 0x001A | 2 bytes | [Status 1]({{site.baseurl}}/technical-reference/list/status-flags#status-1) (statuses 0-15)    |
| 0x001C | 4 bytes | [Status 2]({{site.baseurl}}/technical-reference/list/status-flags#status-2) (statuses 16-47)   |

## Sequence buttons

Each of the five slots is a `u16`, but it is **never used raw** — the engine masks it with `0xF0FF`
everywhere, and bit `0x0100` of *button 1 only* is not a button at all but a finisher flag.

### The button bits

`BattleMenu_ZellDuel_Update` (0x4AF840) builds the recorded input as
`(unsigned __int8)read_pad_pressed_raw(...) | (ctx+20 & 0xF000)` — the low byte from the engine pad
mask plus the D-pad nibble — and compares it against `stored & 0xF0FF`. `BuildZellDuelMenu`
(0x4B0280) picks the on-screen glyph from the *index of the lowest set bit* of the same masked value
(icon id = bit index + 0x80).

Each bit is a remappable **slot**, not a fixed key: the value stored in the kernel never changes,
but which key or pad button performs it depends on the player's controls. The table gives the slot's
default gamepad button and the `ff8input.cfg` line that rebinds it — `Create_ff8input_cfg`
(0x498CB0) writes the fourteen commands in order and `sub_498550` maps each one to its pad bit.

| Value    | Default pad button | `ff8input.cfg` command |
|----------|--------------------|------------------------|
| `0x0001` | L2                 | 7. `RotLt`             |
| `0x0002` | R2                 | 8. `RotRt`             |
| `0x0004` | L1                 | 5. `Toggle`            |
| `0x0008` | R1                 | 6. `Trigger`           |
| `0x0010` | Triangle           | 4. `Menu`              |
| `0x0020` | Circle             | 1. `Select`            |
| `0x0040` | Cross              | 2. `Exit`              |
| `0x0080` | Square             | 3. `Misc`              |
| `0x1000` | Up                 | 11. `Up`               |
| `0x2000` | Right              | 14. `Right`            |
| `0x4000` | Down               | 12. `Down`             |
| `0x8000` | Left               | 13. `Left`             |
| `0xFFFF` | *unused slot*      |                        |

Two more commands exist but cannot appear in a Duel input: `9. Start` (`0x0800`) and
`10. Select` (`0x0100`) are above the low byte the matcher reads — which is exactly why `0x0100`
was free to be reused as the finisher flag below.

> **This corrects an earlier version of this page**, which listed the raw PSX hardware button word
> (directions at `0x0010`-`0x0080`, face buttons at `0x1000`-`0x8000`, finisher at `0x0001`). The
> kernel stores the *engine* pad mask instead, whose two halves are swapped relative to the hardware
> word. The give-away is Dolphin Blow, whose four inputs are `0x0004 0x0008 0x0004 0x0008`: those are
> L1/R1 in the engine mask, but R3/Start in the hardware word — and the PC input layer can never emit
> R3 or Start (`sub_498550` emits `0x0001`-`0x0100`, `0x0800` and `0x1000`-`0x8000`, never `0x0200`
> or `0x0400`). No vanilla entry sets `0x0001` at all.

The pad-button names match the engine pad mask documented for the button-remap table (bits 0-11 =
L2, R2, L1, R1, Triangle, Circle, Cross, Square, Select, L3, R3, Start). The direction bits are
confirmed the same way, through `Create_ff8input_cfg`'s command order, and corroborated by My Final
Heaven reading as a full clockwise circle.

Bits `0x0200` and `0x0400` (L3/R3) are masked off and unreachable anyway — `sub_498550` never emits
them, which is why the Controls menu greys those rows out without an analog pad. Bits 8-11 of
buttons 2-5 are likewise masked off and read by nothing.

`0xFFFF` marks an unused slot. The matcher counts a move's inputs by walking **back** from button 5
while the slot reads `0xFFFF`, so the used slots must be packed from button 1 with no gap in the
middle.

### The finisher flag (bit `0x0100` of button 1)

`BuildZellDuelMenu` reads it from button 1 alone (`v8 = *SequenceButton1 & 0x100`) and turns it into
bit `0x40` of the menu row byte; `BattleMenu_ZellDuel_Update` then selects the state that **closes the
Duel window** (`BattleUI_CloseWindow(6)`) instead of returning to the input loop. In other words, a
move with this bit set **ends the limit break**. Both the matched-input path and the auto-limit path
use it.

Vanilla sets it on exactly the four five-input moves.

### Vanilla sequences

Decoded from `kernel.bin` with the mask applied:

| Move            | Inputs                      | Ends Duel |
|-----------------|-----------------------------|-----------|
| Punch Rush      | ○ ✕                         |           |
| Booya           | → ←                         |           |
| Heel Drop       | ↑ ↓                         |           |
| Mach Kick       | ← ← ○                       |           |
| Dolphin Blow    | L1 R1 L1 R1                 |           |
| Meteor Strike   | ↓ ○ ↑ ○                     |           |
| Burning Rave    | ↓ ↓ ↓ ↓ ○                   | yes       |
| Meteor Barret   | ↑ ✕ ↓ △ ○                   | yes       |
| Different Beat  | △ □ ✕ ○ ↑                   | yes       |
| My Final Heaven | ↑ → ↓ ← △                   | yes       |

The four raw words carrying the finisher bit are Burning Rave `0x4100`, Meteor Barret `0x1100`,
Different Beat `0x0110` and My Final Heaven `0x1100` — always in button 1.
