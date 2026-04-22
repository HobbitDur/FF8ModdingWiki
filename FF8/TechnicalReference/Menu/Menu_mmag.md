---
layout: default
parent: Menu
title: GF tutorial (mtmag.bin file format)
permalink: /technical-reference/menu/mmag/
author: hobbitdur
---

Each entry is 68 bytes

Here a guess from the AI (didn't analyze it) for the first entry:

| Offset | Bytes (hex) | Meaning                       |
|--------|-------------|-------------------------------|
| 0x00   | 18 00       | Entry ID / GF ID? (24)        |
| 0x02   | 08 00       | Type / category (8)           |
| 0x04   | 50 01       | Item/ability ID (336 = 0x150) |
| 0x06   | B8 00       | Unknown (184)                 |
| 0x08   | 0D 00       | Unknown (13)                  |
| 0x0A   | 54 00       | Unknown (84)                  |
| 0x0C   | 98 00       | Unknown (152)                 |
| 0x0E   | 60 00       | Unknown (96)                  |
| 0x10   | 73 23 00 00 | Pointer (29555)               |
| 0x14   | C0 00 00 00 | Flags (192)                   |
| 0x18   | 06 10 FF FF | Unknown (6, 16, -1, -1)       |
| 0x1C   | A9 00       | GF/Ability ID (169)           |
| 0x1E   | 66 A0       | Unknown (102, 160)            |
| 0x20   | 00 00       | Padding                       |
| 0x22   | 00 01       | Unknown (0, 1)                |
| 0x24   | 19 00       | Unknown (25)                  |
| 0x26   | 54 00       | Unknown (84)                  |
| 0x28   | 00 00       | Padding                       |
| 0x2A   | 00 FF       | Flags (0, 255)                |
| 0x2C   | 00 00       | Padding                       |
| 0x2E   | 00 FF       | Flags (0, 255)                |
| 0x30   | 00 00       | Padding                       |
| 0x32   | 00 FF       | Flags (0, 255)                |
| 0x34   | 0D 00       | Unknown (13)                  |
| 0x36   | 06 01       | Quantity / level (6, 1)       |
| 0x38   | 0D 00       | Unknown (13)                  |
| 0x3A   | 16 02       | Unknown (22, 2)               |
| 0x3C   | A9 00       | GF/Ability ID (169)           |
| 0x3E   | 56 00       | Unknown (86, 0)               |
| 0x40   | 00 00       | Padding                       |
| 0x42   | 00 FF       | Flags (0, 255) - terminator   |