---
layout: default
parent: Menu
title: Tutorial books (mtmag.bin file format)
permalink: /technical-reference/menu/mtmag/
author: hobbitdur
---

mtmag.bin defines the three books available from the tutorial menu by pointing at ranges of
[mmag.bin](../mmag/) entries. The file is 3 entries of 4 bytes:

| Offset | Size | Description                              |
|--------|------|----------------------------------------------|
| 0x00   | 1    | First [mmag.bin](../mmag/) entry of the book |
| 0x01   | 1    | Last mmag.bin entry of the book              |
| 0x02   | 2    | Padding                                      |

Retail data (English PC release):

| Entry | Range | Book                       | Tutorial menu program |
|-------|-------|--------------------------------|-----------------------|
| 0     | 43-50 | Battle tutorial (8 pages)      | 25                    |
| 1     | 51-63 | Card rules (13 pages)          | 26                    |
| 2     | 64-67 | Card icon explanation (4 pages) | 31                   |

The tutorial menu stores the selected book's range in `Menu_Magazine_FirstEntry` / `Menu_Magazine_LastEntry`
and starts the matching magazine viewer program, which pages between those two mmag entries.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `Menu_Magazine_FirstEntry` | 0x1D7D3A5 | First mmag entry of the currently open book (global variable/data, not a function) |
| `Menu_Magazine_LastEntry` | 0x1D7D3A6 | Last mmag entry of the currently open book (global variable/data, not a function) |
