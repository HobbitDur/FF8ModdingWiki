---
layout: default
parent: Menu
title: Chocobo World pages (mmag2.bin file format)
permalink: /technical-reference/menu/mmag2/
author: hobbitdur
---

mmag2.bin drives the save-point **Chocobo World screen** (menu program 27): the Mog story slides and the
"Solo RPG" manual pages. It uses **the same 68-byte entry format as [mmag.bin](../mmag/)** — see that page for
the field layout. The file is 12 entries (816 bytes), no header.

Differences from the magazine viewer in how the fields are used:

* **Text overlays** (offset 0x34): the string ids reference the [string section](../mngrp-string-section/)
  raw file 90 (Chocobo World text: story slides = strings 0-4, Solo RPG manual = strings 5-14), loaded to a
  different buffer than the magazines' book text. The text file index at 0x15 is not used.
* **Picture overlays** (offset 0x24): sprite ids 58-76 of the
  [SP2 quad-list table](../mngrpbin-file-format/#the-sp2-quad-list-sprite-format-pos-4) at Pos 4 of mngrp.bin — the high
  sprite ids of that table belong to this screen.
* **Page textures**: all entries use category 6 (base raw file 180): page 0 = raw 180 (story pictures),
  page 1 = raw 181 (manual pictures).

## Entry map (English PC release)

| Entries | Content                                  | Text ids (raw 90) | Page picture |
|---------|----------------------------------------------|-------------------|--------------|
| 0-2     | Story slides (Mog goes treasure hunting)     | 0-4               | raw 180      |
| 3       | "What is Solo RPG?" (manual 1/8)             | 5                 | raw 181      |
| 4-11    | Manual pages 2/8 - 8/8                       | 6-14              | raw 181      |

## Addresses (FF8 PC 2000 EN)

| Address   | Name                                   | Description                                    |
|-----------|----------------------------------------|------------------------------------------------|
| 0x4CFC20  | Menu_ChocoboWorld_Init                 | Program 27 init (reloads cyocobo.bin, music)   |
| 0x4D1D30  | Menu_ChocoboWorld_Draw                 | Draws the screen incl. the mmag2-driven page   |
| 0x4D22F0  | Menu_ChocoboWorld_DrawTextOverlays     | Text overlay slots from raw 90                 |
| 0x4D2270  | Menu_ChocoboWorld_DrawPictureOverlays  | Picture overlay slots from the Pos 4 SP2 table |
| 0x1D2BB74 | mmag2bin                               | Pointer to the loaded mmag2.bin                |
