---
layout: default
parent: Menu
title: Magazine pages (mmag.bin file format)
permalink: /technical-reference/menu/mmag/
author: hobbitdur
---

mmag.bin (a standalone file of the menu archive, loaded at menu startup) drives the in-menu magazine viewer:
each entry describes one magazine page view — the text window, the page picture, up to 4 picture overlays and
up to 4 text overlays. The picture overlays reference [mngrp.bin](../mngrp/) Pos 4, the text overlays reference
the book-text string sections (raw files 87+).

The file is an array of 68-byte entries (69 entries in the English PC release), with no header.
[mmag2.bin](../mmag2/) (the Chocobo World screen pages) uses the same entry format.

## Entry format

| Offset | Size | Description                                                                                     |
|--------|------|-----------------------------------------------------------------------------------------------|
| 0x00   | 2    | Window X (24 in all retail entries)                                                            |
| 0x02   | 2    | Window Y (8)                                                                                   |
| 0x04   | 2    | Window width (336)                                                                             |
| 0x06   | 2    | Window height (184)                                                                            |
| 0x08   | 2    | Page picture X                                                                                 |
| 0x0A   | 2    | Page picture Y                                                                                 |
| 0x0C   | 2    | Page picture width (0 = no picture)                                                            |
| 0x0E   | 2    | Page picture height                                                                            |
| 0x10   | 1    | Picture X scale (multiplied by the zoom factor, /128)                                          |
| 0x11   | 1    | Picture Y scale                                                                                |
| 0x12   | 1    | Picture Z scale                                                                                |
| 0x13   | 1    | Paper background parameter A (PS1 GPU E1 texture page bits)                                    |
| 0x14   | 1    | Paper background parameter B (PS1 GPU E2 texture window bits)                                  |
| 0x15   | 1    | Text file index: the string section loaded is raw file 87 + this value                         |
| 0x16   | 1    | Page texture category (see the category table below)                                          |
| 0x17   | 1    | Page texture page number                                                                       |
| 0x18   | 1    | Weapon index: ORed as a bit into the savemap unlocked-weapons mask, and the weapon's remodel line (from mwepon.bin) is drawn on the page. 0xFF = none. Used by the Weapons Monthly pages (one weapon per page) |
| 0x19   | 1    | Weapon line spacing                                                                            |
| 0x1A   | 1    | Zell Duel move id: unlocked in the savemap and its button combo (from the kernel Duel data) is drawn. 0xFF = none. Used by the Combat King pages |
| 0x1B   | 1    | Angelo move id: unlocked in the savemap. 0xFF = none. Used by the Pet Pals pages               |
| 0x1C   | 2    | Weapon list X                                                                                  |
| 0x1E   | 1    | Weapon list Y                                                                                  |
| 0x1F   | 1    | Weapon quantity column X offset                                                                |
| 0x20   | 2    | Duel combo X                                                                                   |
| 0x22   | 1    | Duel combo Y                                                                                   |
| 0x23   | 1    | Footer flag: 1 = draw the "To be continued"-style footer line (menu string 1/13/28)            |
| 0x24   | 16   | 4 picture overlay slots, 4 bytes each (see below)                                              |
| 0x34   | 16   | 4 text overlay slots, 4 bytes each (see below)                                                 |

### Overlay slots

Both slot arrays use the same 4-byte layout; a slot with id 0xFF is unused:

| Offset | Size | Description                                                     |
|--------|------|---------------------------------------------------------------------|
| 0x00   | 2    | X position (relative to the window position)                        |
| 0x02   | 1    | Y position                                                          |
| 0x03   | 1    | Id                                                                  |

* **Picture overlays** (0x24): the id selects a sprite in the [SP2 quad-list
  table](../mngrp/#the-sp2-quad-list-sprite-format-pos-4) at Pos 4 of mngrp.bin, drawn over the page.
* **Text overlays** (0x34): the id selects a string in the book-text
  [string section](../mngrp-string-section/) (raw file 87 + entry byte 0x15), drawn with the menu text engine.

## Page texture categories

The page texture loader maps the category to a base raw file index inside [mngrp.bin](../mngrp/); the loaded
file is base + page number:

| Category | Base raw file | Content                          |
|----------|---------------|--------------------------------------|
| 0        | 28            | Weapons Monthly issue pictures       |
| 1        | 20            | Combat King pictures                 |
| 2        | 24            | Pet Pals pictures                    |
| 3        | 44            | Occult Fan pictures                  |
| 4        | 48            | Card textures (unused by mmag.bin)   |
| 5        | 71            | Card rules / battle tutorial pictures |
| 6        | 180           | Card icon explanation pictures       |
| other    | -             | The page number is used directly as the raw file index |

## Magazine map (English PC release)

| Entries | Content                                    | Text file (raw) | Page pictures (raw) |
|---------|------------------------------------------------|-----------------|---------------------|
| 0-27    | Weapons Monthly, 7 issues × 4 pages (1st, March...August) | 87 | 28-34 (one per issue) |
| 28-32   | Combat King 001-005 (1 page each)              | 87              | 20                  |
| 33-38   | Pet Pals Vol.1-6 (1 page each)                 | 87              | 24                  |
| 39-42   | Occult Fan I-IV (1 page each)                  | 87              | 44-45               |
| 43-50   | Battle tutorial, 8 pages                       | 88              | 74-75               |
| 51-63   | Card rules, 13 pages                           | 89              | 71                  |
| 64-67   | Card icon explanation, 4 pages                 | 89              | 182                 |
| 68      | Empty terminator entry                         | -               | -                   |

Entries 0-42 are the item-menu magazines: using a magazine item opens the items module's own reader
(a parallel implementation of this viewer, draw functions at 0x4FC990/0x4FD6E0), whose entry range comes from
bytes 2/3 of the item's [mitem.bin](../mitem/) row and which uses a second in-memory copy of mmag.bin
(`mmagbuffer`, 0x1D2BB6C). **The unlock fields (0x18-0x22) are only processed by this item-menu reader** —
reading the page is what unlocks weapons, Duel moves and Angelo moves, every frame the page is displayed.
The tutorial-book viewer ignores those fields (entries 43-67 have them at 0xFF). Entries 43-67 are the three
tutorial-menu books, whose first/last entry indices come from [mtmag.bin](../mtmag/).

## Addresses (FF8 PC 2000 EN)

| Address   | Name                              | Description                                                  |
|-----------|-----------------------------------|--------------------------------------------------------------|
| 0x4C9060  | Menu_Magazine_Update              | Viewer state machine (page turning, zoom)                    |
| 0x4C9330  | Menu_Magazine_Draw                | Draws window, page picture, text overlays, footer            |
| 0x4C9670  | Menu_Magazine_DrawPictureOverlays | Draws the 4 picture overlay slots                            |
| 0x4C95A0  | Menu_Magazine_DrawPageImage       | Draws the scaled page picture quad                           |
| 0x4C9920  | Menu_Magazine_LoadPageTexture     | Loads the page picture TIM from category/page                |
| 0x4C96F0  | Menu_Magazine_DrawPaperBackground | Draws the paper background in 64-pixel strips                |
| 0x1D7D3A5 | Menu_Magazine_FirstEntry          | First mmag entry of the currently open book                  |
| 0x1D7D3A6 | Menu_Magazine_LastEntry           | Last mmag entry of the currently open book                   |
| 0x4FDCA0  | Menu_DrawSp2Sprite                | Generic SP2 quad-list sprite renderer (also cardanm.sp2)     |
| 0x4FC990  | Menu_ItemMagazine_Draw            | Item-menu reader main draw (parallel implementation)         |
| 0x4FD6E0  | Menu_ItemMagazine_DrawPage        | Item-menu page draw, incl. the unlock fields 0x18-0x22       |
| 0x1D773A4 | Menu_BookTextBuffer               | Static buffer receiving the book-text string section         |
| 0x1D2BAF8 | mmagbinbuffer                     | Pointer to the loaded mmag.bin                               |
