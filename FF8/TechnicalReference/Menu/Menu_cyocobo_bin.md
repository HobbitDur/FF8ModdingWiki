---
layout: default
parent: Menu
title: Cyocobo.bin File Format
permalink: /technical-reference/menu/cyocobobin-file-format/
---

# cyocobo.bin

cyocobo.bin (512 bytes, in the menu archive) is the **Chocobo World item conversion table**. When the player
uses the save-point Chocobo World screen to bring items home, each item collected in Chocobo World is converted
into a real FF8 item by a random roll into this table.

## Format

A 128 × 4 byte matrix:

| Type            | Size | Value   | Description                                                       |
|-----------------|------|---------|---------------------------------------------------------------------|
| Byte[128][4]    | 512  | Item ID | `item_id = table[4 * roll + rank]` with `roll = rand() & 0x7F`   |

* The **row** (0-127) is a fresh random roll for every single item transferred.
* The **column** (0-3) is the Chocobo World item rank (class A/B/C/D of the item won in Chocobo World).

So each column is a 128-entry loot pool for one rank; duplicating an item ID on more rows makes it more likely.
In the retail file, column 0 holds 17 distinct high-tier IDs (10 rows each of some), column 3 is dominated by
IDs 109/110/111 (~25 rows each), and columns 1/2 spread over 83/76 distinct IDs.

## Runtime behavior

The conversion loop (in `ChocoboWorld_Prog27Menu_Update`, case of the transfer
screen) accumulates quantities per item ID with a **cap of 100 per ID**, then walks IDs 0-198 to build the
result list shown to the player. Two special cases while building that list:

* An awarded ID of 100 also calls the item-award helper with item 123.
* An awarded ID of 65 is remapped to 110 unless a game flag is set.

A bonus item (one extra unit of ID 65) is added when the transfer includes the special-event flag from the
Chocobo World save.

Unlike tkmnmes or m00X, cyocobo.bin has **no copy inside mngrp.bin**: the standalone file in the menu archive is
the one loaded (by `MenuReadFiles` at boot and again by the Chocobo World menu program init, `Menu_ChocoboWorld_Init`).

## Function addresses

| Function | Address | Description |
|---|---|---|
| `ChocoboWorld_Prog27Menu_Update` | 0x4CFCE0 | Chocobo World screen update, incl. the item-conversion transfer-screen case |
| `Menu_ChocoboWorld_Init` | 0x4CFC20 | Program 27 init (reloads cyocobo.bin, music) |
