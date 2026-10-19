---
layout: default
title: Misc text pointers
nav_order: 32
parent: Kernel
permalink: /technical-reference/main/kernel/misc-text-pointers/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4D08 | 128      | 2 bytes      |

## Sections

Each entry is a **16-bit text offset**, not a native pointer. Index `i` is at
section-relative offset `2 * i`; its string belongs to text section **56**. The EN
previews below are decoded from the vanilla kernel; SolomonRing displays the current
loaded file's text. A readable string does not prove which code consumes it: **Use not
traced** explicitly marks that remaining uncertainty. Placeholder text is retained.

> Entries 37-41 and 101-108 were identified from the scan-screen code path
> (`manageScanText` @ 0xB67EF0) and by decoding `main/kernel.bin` directly.
> The eight element names are **not** words: each is a 2-byte text special code
> (0x055D-0x0564) rendered as an icon glyph. See [Element System]({{site.baseurl}}/technical-reference/battle/element-system/).

| Index | Vanilla file offset | EN text / symbol | Confirmed role |
|---|---|---|---|
| 0 | 0x4D08 | Game over... | Use not traced |
| 1 | 0x4D0A | Escaped | Use not traced |
| 2 | 0x4D0C | GF | Use not traced |
| 3 | 0x4D0E | PAUSE | Use not traced |
| 4 | 0x4D10 | Can't escape | Use not traced |
| 5 | 0x4D12 | Draw failed! | Use not traced |
| 6 | 0x4D14 | Received {RewardItem} | Use not traced |
| 7 | 0x4D16 | learned! | Use not traced |
| 8 | 0x4D18 | s! | Use not traced |
| 9 | 0x4D1A | Received | Use not traced |
| 10 | 0x4D1C | ???? | Use not traced |
| 11 | 0x4D1E |  0123456789ABCDEF:/·, | Use not traced |
| 12 | 0x4D20 | All enemies | Use not traced |
| 13 | 0x4D22 | All party members | Use not traced |
| 14 | 0x4D24 | All | Use not traced |
| 15 | 0x4D26 | No more space | Use not traced |
| 16 | 0x4D28 | Card] | Use not traced |
| 17 | 0x4D2A | Couldn't steal | Use not traced |
| 18 | 0x4D2C | Has nothing | Use not traced |
| 19 | 0x4D2E | Stole | Use not traced |
| 20 | 0x4D30 | Can't select | Use not traced |
| 21 | 0x4D32 | Item received | Use not traced |
| 22 | 0x4D34 | to confirm | Use not traced |
| 23 | 0x4D36 | EXP received | Use not traced |
| 24 | 0x4D38 | {RewardItem}<br>over 100 was discarded | Use not traced |
| 25 | 0x4D3A | End | Use not traced |
| 26 | 0x4D3C | is | Use not traced |
| 27 | 0x4D3E | 's | Use not traced |
| 28 | 0x4D40 | Couldn't find any items! | Use not traced |
| 29 | 0x4D42 | EXP Acquired | Use not traced |
| 30 | 0x4D44 | Current EXP | Use not traced |
| 31 | 0x4D46 | Next LEVEL | Use not traced |
| 32 | 0x4D48 | LEVEL UP! | Use not traced |
| 33 | 0x4D4A | LEVEL | Use not traced |
| 34 | 0x4D4C | HP | Use not traced |
| 35 | 0x4D4E | Status | Use not traced |
| 36 | 0x4D50 | Monster | Use not traced |
| 37 | 0x4D52 | Very weak against | Scan affinity label: "very weak against" |
| 38 | 0x4D54 | Weak against | Scan affinity label: "weak against" |
| 39 | 0x4D56 | Strong against | Scan affinity label: "strong against" |
| 40 | 0x4D58 | has no effect | Scan affinity label: "has no effect" |
| 41 | 0x4D5A | Absorbs | Scan affinity label: "absorbs" |
| 42 | 0x4D5C | attack ineffective | Use not traced |
| 43 | 0x4D5E | attack effective | Use not traced |
| 44 | 0x4D60 | Chance for first strike! | Use not traced |
| 45 | 0x4D62 | Back attacked! | Use not traced |
| 46 | 0x4D64 | Struck first! | Use not traced |
| 47 | 0x4D66 | Back attack! | Use not traced |
| 48 | 0x4D68 | LEVEL UP! | Use not traced |
| 49 | 0x4D6A | Didn't receive EXP | Use not traced |
| 50 | 0x4D6C | Can't turn into a card! | Use not traced |
| 51 | 0x4D6E | Acquired | Use not traced |
| 52 | 0x4D70 | Can't use on GF | Use not traced |
| 53 | 0x4D72 | Not enough money | Use not traced |
| 54 | 0x4D74 | GF recovered HP! | Use not traced |
| 55 | 0x4D76 | Nothing happened | Use not traced |
| 56 | 0x4D78 | is not here | Use not traced |
| 57 | 0x4D7A | KO | Use not traced |
| 58 | 0x4D7C | Poison | Use not traced |
| 59 | 0x4D7E | Petrify | Use not traced |
| 60 | 0x4D80 | Darkness | Use not traced |
| 61 | 0x4D82 | Silence | Use not traced |
| 62 | 0x4D84 | Berserk | Use not traced |
| 63 | 0x4D86 | Zombie | Use not traced |
| 64 | 0x4D88 | ] Found! | Use not traced |
| 65 | 0x4D8A | Times | Use not traced |
| 66 | 0x4D8C | Cast | Use not traced |
| 67 | 0x4D8E | Do over | Use not traced |
| 68 | 0x4D90 | Use indicated magic | Use not traced |
| 69 | 0x4D92 | Turn the slot again | Use not traced |
| 70 | 0x4D94 | AP received | Use not traced |
| 71 | 0x4D96 | [ | Use not traced |
| 72 | 0x4D98 | MiniMog is not here | Use not traced |
| 73 | 0x4D9A | Sleep | Use not traced |
| 74 | 0x4D9C | Haste | Use not traced |
| 75 | 0x4D9E | Slow | Use not traced |
| 76 | 0x4DA0 | Stop | Use not traced |
| 77 | 0x4DA2 | Regen | Use not traced |
| 78 | 0x4DA4 | Protect | Use not traced |
| 79 | 0x4DA6 | Shell | Use not traced |
| 80 | 0x4DA8 | Reflect | Use not traced |
| 81 | 0x4DAA | Aura | Use not traced |
| 82 | 0x4DAC | Curse | Use not traced |
| 83 | 0x4DAE | Doom | Use not traced |
| 84 | 0x4DB0 | Invincible | Use not traced |
| 85 | 0x4DB2 | Petrifying | Use not traced |
| 86 | 0x4DB4 | Float | Use not traced |
| 87 | 0x4DB6 | Confuse | Use not traced |
| 88 | 0x4DB8 | 's Level went  | Use not traced |
| 89 | 0x4DBA | up by | Use not traced |
| 90 | 0x4DBC | Double | Use not traced |
| 91 | 0x4DBE | Triple | Use not traced |
| 92 | 0x4DC0 | Defend | Use not traced |
| 93 | 0x4DC2 | Physical attack ineffective | Use not traced |
| 94 | 0x4DC4 | Magic ineffective | Use not traced |
| 95 | 0x4DC6 | down by | Use not traced |
| 96 | 0x4DC8 | Back attack | Use not traced |
| 97 | 0x4DCA | Vit 0 | Use not traced |
| 98 | 0x4DCC | Angel Wing | Use not traced |
| 99 | 0x4DCE | Fly | Use not traced |
| 100 | 0x4DD0 | Can't use magic | Use not traced |
| 101 | 0x4DD2 | Fire element icon (05 5D) | Element name: **Fire** — 2 bytes `05 5D` (text special code 0x055D, icon glyph) |
| 102 | 0x4DD4 | Ice element icon (05 5E) | Element name: **Ice** — 2 bytes `05 5E` |
| 103 | 0x4DD6 | Thunder element icon (05 5F) | Element name: **Thunder** — 2 bytes `05 5F` |
| 104 | 0x4DD8 | Earth element icon (05 60) | Element name: **Earth** — 2 bytes `05 60` |
| 105 | 0x4DDA | Poison element icon (05 61) | Element name: **Poison** — 2 bytes `05 61` |
| 106 | 0x4DDC | Wind element icon (05 62) | Element name: **Wind** — 2 bytes `05 62` |
| 107 | 0x4DDE | Water element icon (05 63) | Element name: **Water** — 2 bytes `05 63` |
| 108 | 0x4DE0 | Holy element icon (05 64) | Element name: **Holy** — 2 bytes `05 64` |
| 109 | 0x4DE2 | GF received {RewardAmount}AP! | Use not traced |
| 110 | 0x4DE4 | {RewardItem}'s Card | Use not traced |
| 111 | 0x4DE6 | Raising GF | Use not traced |
| 112 | 0x4DE8 | Couldn't Devour! | Use not traced |
| 113 | 0x4DEA | ????? | Use not traced |
| 114 | 0x4DEC | Undead | Use not traced |
| 115 | 0x4DEE | ] | Use not traced |
| 116 | 0x4DF0 | wore off! | Use not traced |
| 117 | 0x4DF2 | was blown away! | Use not traced |
| 118 | 0x4DF4 | ! | Use not traced |
| 119 | 0x4DF6 | s | Use not traced |
| 120 | 0x4DF8 | learned | Use not traced |
| 121 | 0x4DFA | GF  | Use not traced |
| 122 | 0x4DFC | Dummy | Use not traced |
| 123 | 0x4DFE | Dummy | Use not traced |
| 124 | 0x4E00 | Dummy | Use not traced |
| 125 | 0x4E02 | Dummy | Use not traced |
| 126 | 0x4E04 | ! | Use not traced |
| 127 | 0x4E06 | learned | Use not traced |

## Section Structure

| Offset | Length  | Description    |
|--------|---------|----------------|
| 0x0000 | 2 bytes | Offset to text |
