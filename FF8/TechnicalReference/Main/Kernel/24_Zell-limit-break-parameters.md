---
layout: default
title: Duel parameters
nav_order: 24
parent: Kernel
permalink: /technical-reference/main/kernel/duel-parameters/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x49F8 | 1        | 100 bytes    |

## Overview

This section is the **Duel move graph** for Zell's "Duel" limit break: **25 sequence entries** of 4
bytes each — one `StartMove` plus three `Next Sequence` bytes.

- `StartMove` is the Duel move performed while that sequence is current (a value `>= 6` ends the Duel
  with a finisher, handled by `sub_4852B0`).
- The three `Next Sequence` bytes are the sequence indices the Duel jumps to next, chosen by the
  player's button input from the current move.

The **entry point** into this table is not stored here — it's the *Duel Start Sequence* byte for the
character's crisis level in the [Misc section](../misc/) (0x30/0x32/0x34/0x36). `linkedToZellDuel`
seeds the current sequence from that byte, then `sub_4852B0` walks the graph move by move.

## Section Structure

| Offset | Length | Description        |
|--------|--------|--------------------|
| 0x0000 | 1 byte | [[StartMove 0      |Zell's Duel Moves]]   |
| 0x0001 | 1 byte | Next Sequence 0_1  |
| 0x0002 | 1 byte | Next Sequence 0_2  |
| 0x0003 | 1 byte | Next Sequence 0_3  |
| 0x0004 | 1 byte | [[StartMove 1      |Zell's Duel Moves]]   |
| 0x0005 | 1 byte | Next Sequence 1_1  |
| 0x0006 | 1 byte | Next Sequence 1_2  |
| 0x0007 | 1 byte | Next Sequence 1_3  |
| 0x0008 | 1 byte | [[StartMove 2      |Zell's Duel Moves]]   |
| 0x0009 | 1 byte | Next Sequence 2_1  |
| 0x000A | 1 byte | Next Sequence 2_2  |
| 0x000B | 1 byte | Next Sequence 2_3  |
| 0x000C | 1 byte | [[StartMove 3      |Zell's Duel Moves]]   |
| 0x000D | 1 byte | Next Sequence 3_1  |
| 0x000E | 1 byte | Next Sequence 3_2  |
| 0x000F | 1 byte | Next Sequence 3_3  |
| 0x0010 | 1 byte | [[StartMove 4      |Zell's Duel Moves]]   |
| 0x0011 | 1 byte | Next Sequence 4_1  |
| 0x0012 | 1 byte | Next Sequence 4_2  |
| 0x0013 | 1 byte | Next Sequence 4_3  |
| 0x0014 | 1 byte | [[StartMove 5      |Zell's Duel Moves]]   |
| 0x0015 | 1 byte | Next Sequence 5_1  |
| 0x0016 | 1 byte | Next Sequence 5_2  |
| 0x0017 | 1 byte | Next Sequence 5_3  |
| 0x0018 | 1 byte | [[StartMove 6      |Zell's Duel Moves]]   |
| 0x0019 | 1 byte | Next Sequence 6_1  |
| 0x001A | 1 byte | Next Sequence 6_2  |
| 0x001B | 1 byte | Next Sequence 6_3  |
| 0x001C | 1 byte | [[StartMove 7      |Zell's Duel Moves]]   |
| 0x001D | 1 byte | Next Sequence 7_1  |
| 0x001E | 1 byte | Next Sequence 7_2  |
| 0x001F | 1 byte | Next Sequence 7_3  |
| 0x0020 | 1 byte | [[StartMove 8      |Zell's Duel Moves]]   |
| 0x0021 | 1 byte | Next Sequence 8_1  |
| 0x0022 | 1 byte | Next Sequence 8_2  |
| 0x0023 | 1 byte | Next Sequence 8_3  |
| 0x0024 | 1 byte | [[StartMove 9      |Zell's Duel Moves]]   |
| 0x0025 | 1 byte | Next Sequence 9_1  |
| 0x0026 | 1 byte | Next Sequence 9_2  |
| 0x0027 | 1 byte | Next Sequence 9_3  |
| 0x0028 | 1 byte | [[StartMove 10     |Zell's Duel Moves]]  |
| 0x0029 | 1 byte | Next Sequence 10_1 |
| 0x002A | 1 byte | Next Sequence 10_2 |
| 0x002B | 1 byte | Next Sequence 10_3 |
| 0x002C | 1 byte | [[StartMove 11     |Zell's Duel Moves]]  |
| 0x002D | 1 byte | Next Sequence 11_1 |
| 0x002E | 1 byte | Next Sequence 11_2 |
| 0x002F | 1 byte | Next Sequence 11_3 |
| 0x0030 | 1 byte | [[StartMove 12     |Zell's Duel Moves]]  |
| 0x0031 | 1 byte | Next Sequence 12_1 |
| 0x0032 | 1 byte | Next Sequence 12_2 |
| 0x0033 | 1 byte | Next Sequence 12_3 |
| 0x0034 | 1 byte | [[StartMove 13     |Zell's Duel Moves]]  |
| 0x0035 | 1 byte | Next Sequence 13_1 |
| 0x0036 | 1 byte | Next Sequence 13_2 |
| 0x0037 | 1 byte | Next Sequence 13_3 |
| 0x0038 | 1 byte | [[StartMove 14     |Zell's Duel Moves]]  |
| 0x0039 | 1 byte | Next Sequence 14_1 |
| 0x003A | 1 byte | Next Sequence 14_2 |
| 0x003B | 1 byte | Next Sequence 14_3 |
| 0x003C | 1 byte | [[StartMove 15     |Zell's Duel Moves]]  |
| 0x003D | 1 byte | Next Sequence 15_1 |
| 0x003E | 1 byte | Next Sequence 15_2 |
| 0x003F | 1 byte | Next Sequence 15_3 |
| 0x0040 | 1 byte | [[StartMove 16     |Zell's Duel Moves]]  |
| 0x0041 | 1 byte | Next Sequence 16_1 |
| 0x0042 | 1 byte | Next Sequence 16_2 |
| 0x0043 | 1 byte | Next Sequence 16_3 |
| 0x0044 | 1 byte | [[StartMove 17     |Zell's Duel Moves]]  |
| 0x0045 | 1 byte | Next Sequence 17_1 |
| 0x0046 | 1 byte | Next Sequence 17_2 |
| 0x0047 | 1 byte | Next Sequence 17_3 |
| 0x0048 | 1 byte | [[StartMove 18     |Zell's Duel Moves]]  |
| 0x0049 | 1 byte | Next Sequence 18_1 |
| 0x004A | 1 byte | Next Sequence 18_2 |
| 0x004B | 1 byte | Next Sequence 18_3 |
| 0x004C | 1 byte | [[StartMove 19     |Zell's Duel Moves]]  |
| 0x004D | 1 byte | Next Sequence 19_1 |
| 0x004E | 1 byte | Next Sequence 19_2 |
| 0x004F | 1 byte | Next Sequence 19_3 |
| 0x0050 | 1 byte | [[StartMove 20     |Zell's Duel Moves]]  |
| 0x0051 | 1 byte | Next Sequence 20_1 |
| 0x0052 | 1 byte | Next Sequence 20_2 |
| 0x0053 | 1 byte | Next Sequence 20_3 |
| 0x0054 | 1 byte | [[StartMove 21     |Zell's Duel Moves]]  |
| 0x0055 | 1 byte | Next Sequence 21_1 |
| 0x0056 | 1 byte | Next Sequence 21_2 |
| 0x0057 | 1 byte | Next Sequence 21_3 |
| 0x0058 | 1 byte | [[StartMove 22     |Zell's Duel Moves]]  |
| 0x0059 | 1 byte | Next Sequence 22_1 |
| 0x005A | 1 byte | Next Sequence 22_2 |
| 0x005B | 1 byte | Next Sequence 22_3 |
| 0x005C | 1 byte | [[StartMove 23     |Zell's Duel Moves]]  |
| 0x005D | 1 byte | Next Sequence 23_1 |
| 0x005E | 1 byte | Next Sequence 23_2 |
| 0x005F | 1 byte | Next Sequence 23_3 |
| 0x0060 | 1 byte | [[StartMove 24     |Zell's Duel Moves]]  |
| 0x0061 | 1 byte | Next Sequence 24_1 |
| 0x0062 | 1 byte | Next Sequence 24_2 |
| 0x0063 | 1 byte | Next Sequence 24_3 |