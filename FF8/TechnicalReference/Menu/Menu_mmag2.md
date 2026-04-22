---
layout: default
parent: Menu
title: ChocoboWorld items (mtmag2.bin file format)
permalink: /technical-reference/menu/mmag2/
author: hobbitdur
---

Seems to be related to choco World item/reward database.

Each entry is 68 bytes, to probably 11 entries.

Here a guess from the AI (didn't analyze it) for the first entry:

| Offset | Bytes (hex) | Bytes (dec) | Possible meaning                         |
|--------|-------------|-------------|------------------------------------------|
| 0x00   | 18 00       | 24, 0       | Word: Entry ID or item type              |
| 0x02   | 38 00       | 56, 0       | Word: Unknown                            |
| 0x04   | 50 01       | 336, 1      | Word: Item ID or quantity? (336 = 0x150) |
| 0x06   | 9E 00       | 158, 0      | Word: Unknown                            |
| 0x08   | 0D 00       | 13, 0       | Word: Unknown                            |
| 0x0A   | 54 00       | 84, 0       | Word: Unknown                            |
| 0x0C   | 00 00       | 0, 0        | Word: Padding/unused                     |
| 0x0E   | 00 00       | 0, 0        | Word: Padding/unused                     |
| 0x10   | 73 23 00 00 | 29555, 0    | Dword: Pointer or value                  |
| 0x14   | C0 05 06 00 | 1472, 6, 0  | Unknown (multiple bytes)                 |
| 0x18   | FF FF FF FF | -1          | 4 bytes: Sentinel/flag                   |
| 0x1C   | A9 00       | 169, 0      | Word: GF or item ID? (169 = A9)          |
| 0x1E   | 66 80       | 102, 128    | Word: Unknown                            |
| 0x20   | 00 00       | 0, 0        | Word: Padding                            |
| 0x22   | 00 00       | 0, 0        | Word: Padding                            |
| 0x24   | 0A 00       | 10, 0       | Word: Quantity or level                  |
| 0x26   | 0C 3A       | 12, 58      | Word: Unknown (0x3A0C = 14860)           |
| 0x28   | 00 00       | 0, 0        | Word: Padding                            |
| 0x2A   | 00 FF       | 0, 255      | Word: Flags                              |
| 0x2C   | 00 00       | 0, 0        | Word: Padding                            |
| 0x2E   | 00 FF       | 0, 255      | Word: Flags                              |
| 0x30   | 00 00       | 0, 0        | Word: Padding                            |
| 0x32   | 00 FF       | 0, 255      | Word: Flags                              |
| 0x34   | 93 00       | 147, 0      | Word: Spell/ability ID? (147 = 0x93)     |
| 0x36   | 06 00       | 6, 0        | Word: Quantity                           |
| 0x38   | 0D 00       | 13, 0       | Word: Unknown                            |
| 0x3A   | 76 01       | 118, 1      | Word: Unknown (0x176 = 374)              |
| 0x3C   | A9 00       | 169, 0      | Word: GF or item ID (same as 0x1C)       |
| 0x3E   | 56 FF       | 86, 255     | Word: Unknown                            |
| 0x40   | 00 00       | 0, 0        | Word: Padding                            |
| 0x42   | 00 FF       | 0, 255      | Word: Flags (terminator?)                |