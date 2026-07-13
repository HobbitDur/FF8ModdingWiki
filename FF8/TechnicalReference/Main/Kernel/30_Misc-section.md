---
layout: default
title: Misc
nav_order: 31
parent: Kernel
permalink: /technical-reference/main/kernel/misc/
---

# Misc Data Section

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4CCC | 6        | Various      |


## Sections

| Offset | Ability                     | Length   |
|--------|-----------------------------|----------|
| 0x4CCC | Status Timers               | 14 bytes |
| 0x4CDA | ATB Speed Multiplier        | 1 byte   |
| 0x4CDB | Dead Timer                  | 1 byte   |
| 0x4CDC | Status Limit Effects        | 32 bytes |
| 0x4CFC | Duel Timers and Start Moves | 8 bytes  |
| 0x4D04 | Shot Timers                 | 4 bytes  |


## Section Structure

| Offset | Length | Description                        |
|--------|--------|------------------------------------|
| 0x0000 | 1 byte | Sleep Timer                        |
| 0x0001 | 1 byte | Haste Timer                        |
| 0x0002 | 1 byte | Slow  Timer                        |
| 0x0003 | 1 byte | Stop Timer                         |
| 0x0004 | 1 byte | Regen Timer                        |
| 0x0005 | 1 byte | Protect Timer                      |
| 0x0006 | 1 byte | Shell Timer                        |
| 0x0007 | 1 byte | Reflect Timer                      |
| 0x0008 | 1 byte | Aura Timer                         |
| 0x0009 | 1 byte | Curse Timer                        |
| 0x000A | 1 byte | Doom Timer                         |
| 0x000B | 1 byte | Invincible Timer                   |
| 0x000C | 1 byte | Petrifying Timer                   |
| 0x000D | 1 byte | Float Timer                        |
| 0x000E | 1 byte | ATB Speed Multiplier               |
| 0x000F | 1 byte | Dead Timer                         |
| 0x0010 | 1 byte | Death Limit Effect                 |
| 0x0011 | 1 byte | Poison Limit Effect                |
| 0x0012 | 1 byte | Petrify Limit Effect               |
| 0x0013 | 1 byte | Darkness Limit Effect              |
| 0x0014 | 1 byte | Silence Limit Effect               |
| 0x0015 | 1 byte | Berserk Limit Effect               |
| 0x0016 | 1 byte | Zombie Limit Effect                |
| 0x0017 | 1 byte | Unknown Status Limit Effect        |
| 0x0018 | 1 byte | Sleep Limit Effect                 |
| 0x0019 | 1 byte | Haste Limit Effect                 |
| 0x001A | 1 byte | Slow Limit Effect                  |
| 0x001B | 1 byte | Stop Limit Effect                  |
| 0x001C | 1 byte | Regen Limit Effect                 |
| 0x001D | 1 byte | Protect Limit Effect               |
| 0x001E | 1 byte | Shell Limit Effect                 |
| 0x001F | 1 byte | Reflect Limit Effect               |
| 0x0020 | 1 byte | Aura Limit Effect                  |
| 0x0021 | 1 byte | Curse Limit Effect                 |
| 0x0022 | 1 byte | Doom Limit Effect                  |
| 0x0023 | 1 byte | Invincible Limit Effect            |
| 0x0024 | 1 byte | Petrifying Limit Effect            |
| 0x0025 | 1 byte | Float Limit Effect                 |
| 0x0026 | 1 byte | Confusion Limit Effect             |
| 0x0027 | 1 byte | Drain Limit Effect                 |
| 0x0028 | 1 byte | Eject Limit Effect                 |
| 0x0029 | 1 byte | Double Limit Effect                |
| 0x002A | 1 byte | Triple Limit Effect                |
| 0x002B | 1 byte | Defend Limit Effect                |
| 0x002C | 1 byte | Unknown Status Limit Effect        |
| 0x002D | 1 byte | Unknown Status Limit Effect        |
| 0x002E | 1 byte | Charged Limit Effect               |
| 0x002F | 1 byte | Back Attack Limit Effect           |
| 0x0030 | 1 byte | Duel Start Sequence Crisis Level 1 |
| 0x0031 | 1 byte | Duel Timer Crisis Level 1          |
| 0x0032 | 1 byte | Duel Start Sequence Crisis Level 2 |
| 0x0033 | 1 byte | Duel Timer Crisis Level 2          |
| 0x0034 | 1 byte | Duel Start Sequence Crisis Level 3 |
| 0x0035 | 1 byte | Duel Timer Crisis Level 3          |
| 0x0036 | 1 byte | Duel Start Sequence Crisis Level 4 |
| 0x0037 | 1 byte | Duel Timer Crisis Level 4          |
| 0x0038 | 1 byte | Shot Timer Crisis Level 1          |
| 0x0039 | 1 byte | Shot Timer Crisis Level 2          |
| 0x003A | 1 byte | Shot Timer Crisis Level 3          |
| 0x003B | 1 byte | Shot Timer Crisis Level 4          |

## Duel / Shot crisis-level fields (0x30–0x3B)

These drive **Zell's "Duel"** and **Irvine's "Shot"** limit breaks, which both scale with the
character's crisis level (0–3, higher = lower HP / stronger limit).

- **Duel Start Sequence (CL1–4)** — the starting index into the [Duel move table](../zell-limit-break-parameters/)
  (section 24, *Duel Params*). When a Duel begins, `linkedToZellDuel` reads the byte for the current
  crisis level (`K_MISC[0x2E + 2·crisis_level]`) and uses it to seed the "current sequence" pointer.
  The per-tick Duel driver (`sub_4852B0`) then performs `duelMoves[seq].StartMove`, and the player's
  button input selects one of that entry's *Next Sequence* bytes to advance to the next move. In short:
  this byte decides **which move-chain Zell opens the Duel with at each crisis level**.
- **Duel Timer (CL1–4)** — length of the Duel input window at that crisis level (higher crisis = longer),
  loaded alongside the start sequence.
- **Shot Timer (CL1–4)** — the equivalent input-window duration for Irvine's Shot at each crisis level.