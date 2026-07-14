---
layout: default
title: Menu abilities
nav_order: 19
parent: Kernel
permalink: /technical-reference/main/kernel/menu-abilities/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x43C0 | 24       | 8 bytes      |

## Sections

| Offset | Ability        |
|--------|----------------|
| 0x43C0 | Haggle         |
| 0x43C8 | Sell-High      |
| 0x43D0 | Familiar       |
| 0x43D8 | Call Shop      |
| 0x43E0 | Junk Shop      |
| 0x43E8 | T Mag-RF       |
| 0x43F0 | I Mag-RF       |
| 0x43F8 | F Mag-RF       |
| 0x4400 | L Mag-RF       |
| 0x4408 | Time Mag-RF    |
| 0x4410 | ST Mag-RF      |
| 0x4418 | Supt Mag-RF    |
| 0x4420 | Forbid Mag-RF  |
| 0x4428 | Recov Med-RF   |
| 0x4430 | ST Med-RF      |
| 0x4438 | Ammo-RF        |
| 0x4440 | Tool-RF        |
| 0x4448 | Forbid Med-RF  |
| 0x4450 | GFRecov Med-RF |
| 0x4458 | GFAbl Med-RF   |
| 0x4460 | Mid Mag-RF     |
| 0x4468 | High Mag-RF    |
| 0x4470 | Med LV Up      |
| 0x4780 | Card Mod       |

## Section Structure

| Offset | Length  | Description                                                                           |
|--------|---------|---------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to ability name                                                                |
| 0x0002 | 2 bytes | Offset to ability description                                                         |
| 0x0004 | 1 byte  | AP Required to learn ability                                                          |
| 0x0005 | 1 byte  | Refine table (m00X file index) — which Refine data table this ability's item list is drawn from. `Menu_Prog19_RefineMenu_Init` switches on this byte to load a pair of mngrp resource files: `0`=Magic Refine, `1`=Tool/Medicine Refine, `2`=Mid/High Magic Refine, `3`=LV Up Refine, `4`=Card Mod. `4` also builds its on-screen list from the cards you currently own, but it still loads and slices a real recipe table (section 192) like the others. `255`/`128`/`129` (Haggle, Sell-High, Familiar, Call Shop, Junk Shop) aren't Refine abilities at all and ignore Start/End offset |
| 0x0006 | 1 byte  | Start offset — start of this ability's **inclusive** slice of its Refine table's records. `Menu_Prog19_RefineMenu_Init` computes `count = End offset - Start offset + 1` and offsets the table pointer by `8 * Start offset` (each record is 8 bytes) |
| 0x0007 | 1 byte  | End offset — end of this ability's inclusive slice (must be ≥ Start offset). Abilities sharing the same Refine table use non-overlapping slices, e.g. T Mag-RF (table 0, 0-6) and I Mag-RF (table 0, 7-13) split the same loaded item list by element |

## Refine table record format (menu.fs, not kernel.bin)

The item/magic conversions themselves are **not** in kernel.bin — they live in `menu.fs`'s `mngrp.bin`, in the mngrp section pair each table loads: `188`/`196` for table 0, `189`/`197` for table 1, `190`/`198` for table 2, `191`/`199` for table 3, **`192`/`200` for table 4 (Card Mod)** (`Menu_Prog19_RefineMenu_Init` @ 0x4D7180). Card Mod's on-screen list is built at runtime from the cards you own, but the card→item recipes it slices with Start/End offset are still this static section 192. Decoded via `sub_4D9600`/`sub_4D9660` (the Refine screen's row-name resolvers), each record is 8 bytes:

| Offset | Length | Field |
|--------|--------|-------|
| 0x00 | 2 bytes | Display text offset (not needed to decode the conversion — names are resolved from the item/magic/card lists directly) |
| 0x02 | 2 bytes | Output quantity |
| 0x04 | 1 byte | Source quantity required |
| 0x05 | 1 byte | Source material id — **item** id for tables 0/1/3, **magic** id for table 2, **card** id for table 4 |
| 0x06 | 1 byte | Unconfirmed (constant `1` in every sample checked) |
| 0x07 | 1 byte | Destination material id — **magic** id for tables 0/2, **item** id for tables 1/3/4 |

Verified against the retail `menu.fs` and matches the well-known FF8 Refine chart, e.g. T Mag-RF: `1x Coral Fragment → 20x Thundara`, `1x Dynamo Stone → 20x Thundaga`, ...; Mid Mag-RF: `1x Fire → 1x Fira`, ...; Card Mod: `1x Geezard → 5x Screw`, `1x Fungar → 1x M-Stone Piece`, `1x Blobra → 1x Rune Armlet`, ...

SolomonRing's Menu Abilities tab can load `mngrphd.bin`/`mngrp.bin` and show the decoded table for the selected ability directly (reference only — this data isn't part of kernel.bin, so there's nothing to save back).