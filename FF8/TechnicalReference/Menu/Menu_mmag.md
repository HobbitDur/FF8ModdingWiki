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
| 0x08   | 2    | Paper mat X (relative to the window, see [the paper mat](#the-paper-mat-0x08-0x12))            |
| 0x0A   | 2    | Paper mat Y                                                                                    |
| 0x0C   | 2    | Paper mat width (0 = not drawn)                                                                |
| 0x0E   | 2    | Paper mat height (0 = not drawn)                                                               |
| 0x10   | 1    | Paper mat red (multiplied by the zoom colour byte, /128)                                       |
| 0x11   | 1    | Paper mat green                                                                                |
| 0x12   | 1    | Paper mat blue                                                                                 |
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
| 0x23   | 1    | Footer flag: 1 = draw the footer line, menu string 1/13/28 ("{CrossLeft} {CrossRight} to scroll {Circle} to go to Tutorial"), centred at x = (336 - text width) / 2 + 24, y = 200. Only the multi-page books set it |
| 0x24   | 16   | 4 picture overlay slots, 4 bytes each (see below)                                              |
| 0x34   | 16   | 4 text overlay slots, 4 bytes each (see below)                                                 |

### The paper mat (0x08-0x12)

These seven bytes do **not** describe the page picture, and 0x10-0x12 are a colour rather than a
scale. `Menu_Magazine_DrawPageImage` (0x4C95A0) builds a single `GP0(0x62)` primitive — a
monochrome, semi-transparent rectangle with **no texture coordinates at all** — whose R/G/B are the
three bytes at 0x10-0x12, each multiplied by the matching byte of the zoom colour and divided by
128 (so 128 = unchanged):

```
prim.r = zoom.b0 * entry[0x10] / 128
prim.g = zoom.b1 * entry[0x11] / 128
prim.b = zoom.b2 * entry[0x12] / 128
prim.code = 0x62                      // monochrome rect, variable size, semi-transparent
prim.xy   = window.xy + entry[0x08..0x0B]
prim.wh   = entry[0x0C..0x0F]
```

It is the tinted mat drawn *behind* the page art: the art itself is a
[picture overlay](#overlay-slots). Entry 0's (115, 35, 0) is the sepia backing of the Lion Heart
photo, and the Pet Pals pages use it as the reddish frame around the dog. Combat King has no
picture overlay at all and uses the mat alone, as the banner behind its Duel move name.

Both the width and the height must be non-zero for it to be drawn. The entries that want no mat do
not use zeroes: they store (255, 255, 255, 255) with a (0, 0, 0) tint, which lands a black rectangle
at (279, 263) — off screen.

### Overlay slots

Both slot arrays use the same 4-byte layout; a slot with id 0xFF is unused:

| Offset | Size | Description                                                     |
|--------|------|---------------------------------------------------------------------|
| 0x00   | 2    | X position (relative to the window position)                        |
| 0x02   | 1    | Y position                                                          |
| 0x03   | 1    | Id                                                                  |

* **Picture overlays** (0x24): the id selects a sprite in the [SP2 quad-list
  table](../mngrp/#the-sp2-quad-list-sprite-format-pos-4) at Pos 4 of mngrp.bin (raw file 7), drawn
  over the page. **These carry the page art.** Their quads sample the page picture directly: every
  magazine quad has texpage `0x00AE` = VRAM (896, 0) in 8bpp — exactly where the page picture TIM
  declares itself — and CLUT `0x36A0` = VRAM (512, 218), the TIM's own (single) CLUT row. A quad is
  therefore a plain crop of the decoded TIM, at the slot's position plus the quad's own draw offset.
* **Text overlays** (0x34): the id selects a string in the book-text
  [string section](../mngrp-string-section/) (raw file 87 + entry byte 0x15), drawn with the menu text engine.

## Draw order

`Menu_Magazine_Draw` (0x4C9330) fills a PSX ordering table, so the primitives it adds last are the
ones drawn first. Back to front, a page is:

1. the paper background (`Menu_Magazine_DrawPaperBackground`, 0x4C96F0)
2. the menu window gradient (`BattleUI_DrawWindowBackground`)
3. the [paper mat](#the-paper-mat-0x08-0x12)
4. the picture overlays
5. the text overlays, then the footer line when byte 0x23 is set

The paper background is drawn as 64px-wide vertical strips across the window width, textured from
the E1/E2 bits at 0x13/0x14. In every retail entry these are E1 = 0x00 and E2 = 0xC0, which give
texpage VRAM (896, 0) and a texture window of mask (28, 28) offset (0, 24): the U/V are wrapped to
0-31 and 192-223, i.e. a single 32x32 tile at VRAM (896, 192)-(927, 223), just below the 256x192
page picture TIM loaded at the same texpage.

That parchment tile is **[mngrp.bin](../mngrp/) raw file 12**: a standalone 2048-byte file holding
one 32x32 8bpp TIM whose header places its image at VRAM (896, 192) and its CLUT at (512, 219) — a
row below the page pictures' shared CLUT at (512, 218). It is the only TIM in the game data
declaring that placement, and it stays resident while the page TIMs swap in above it. It is
uploaded when a book opens: `Menu_Tutorial_Update` case 14 calls
`Menu_LoadMngrpTextureAsync(12, staging)` right after loading the SP2 table (raw 7), and the
texture loader sends the TIM to the emulated VRAM at its header-declared placement. The menu
window fill (`BattleUI_DrawWindowBackground`, coloured by the player's Config window colour) is
blended over the paper, which is why the pages read as darkened parchment in game.

## Page texture categories

The page texture loader maps the category to a base raw file index inside [mngrp.bin](../mngrp/); the loaded
file is base + page number:

| Category | Base raw file | Content                          |
|----------|---------------|--------------------------------------|
| 0        | 28            | Weapons Monthly issue pictures       |
| 1        | 20            | Loaded by the Combat King pages, but never drawn (see below) |
| 2        | 24            | Pet Pals pictures                    |
| 3        | 44            | Occult Fan pictures                  |
| 4        | 48            | Card textures (unused by mmag.bin)   |
| 5        | 71            | Card rules / battle tutorial pictures |
| 6        | 180           | Card icon explanation pictures       |
| other    | -             | The page number is used directly as the raw file index |

A page texture is only ever sampled through the [picture overlays](#overlay-slots) — nothing else
draws it. The five Combat King entries (28-32) have no picture overlay at all, so their texture is
loaded into VRAM and then never read. Category 1 is theirs alone, and raw file 20 is in fact a
byte-identical copy of raw file 28, the Weapons Monthly weapons: the reference is vestigial, and
those pages have no picture. What fills their banner is the
[Duel combo](#the-unlock-block-0x18-0x22).

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
(a parallel implementation of this viewer, draw functions `Menu_ItemMagazine_Draw`/`Menu_ItemMagazine_DrawPage`),
whose entry range comes from bytes 2/3 of the item's [mitem.bin](../mitem/) row and which uses a second
in-memory copy of mmag.bin (`mmagbuffer`). **The unlock fields (0x18-0x22) are only processed by this item-menu reader** —
reading the page is what unlocks weapons, Duel moves and Angelo moves, every frame the page is displayed.
The tutorial-book viewer ignores those fields (entries 43-67 have them at 0xFF). Entries 43-67 are the three
tutorial-menu books, whose first/last entry indices come from [mtmag.bin](../mtmag/).

## The unlock block (0x18-0x22)

`Menu_ItemMagazine_DrawPage` both applies and draws it. Each field sets its savemap bit every frame
the page is up — that is the whole unlock mechanism — and two of the three also draw:

* **Weapon index (0x18)** — ORs `1 << index` into `SG_PARTY_BATTLE.unlocked_weapons`, then draws the
  weapon's remodel line from [mwepon.bin](../mwepon/) (`mweaponbuffer + 12 * index + 4`, four
  {item id, quantity} pairs, empty ids skipped). Per row: the item's type icon at
  (`weapon_list_x`, `weapon_list_y` - 2), its name at `weapon_list_x + 14`, and the quantity
  **right-aligned** on `weapon_list_x + weapon_quantity_column_x` (`menu_draw_number_rightaligned`).
  Rows step down by `weapon_line_spacing` (0x19). The item name comes from the kernel
  (`getTextBattleItem`), and the type icon is `byte_B88024[mitem.bin row's item type] + 223`, i.e.
  one of [icon.sp1](../icon-sp1/) ids 223-229. `byte_B88024` is a 24-byte table indexed by the
  item type: `0,0,0,1,1,1,2,3,4,5,6,1,3,3,3,3,6,1,1,6,6,0,0,0`.
* **Duel move (0x1A)** — ORs `1 << id` into `SG_LIMIT_BREAK_ZELL`, then draws the move's button
  combo from the kernel's [Duel section](../../kernel/#duel): up to 5 `u16` codes at offset 16 of the
  32-byte entry, terminated by 0xFFFF. Buttons start at (`duel_combo_x`, `duel_combo_y`) and step
  40 px right, with separator icon 55 drawn 16 px left of every button after the first.

  A button code is a pad bitmask, and its icon is
  `128 + (index of the lowest set bit of code & 0xF0FF)` — an [icon.sp1](../icon-sp1/) id. The mask
  drops bits 8-11, which is why the icon ids the combos actually reach are 128-135 and 140-143:

  | Bit | 0  | 1  | 2  | 3  | 4 | 5 | 6 | 7 | 8-11 (masked out) | 12-15 |
  |-----|----|----|----|----|---|---|---|---|-------------------|-------|
  | Icon | 128 | 129 | 130 | 131 | 132 | 133 | 134 | 135 | 136-139 | 140-143 |
  | Button | L2 | R2 | L1 | R1 | Triangle | Circle | Cross | Square | Select, L3, R3, Start | the four d-pad directions |

  So Dolphin Blow (`04 08 04 08`) is L1 R1 L1 R1, and My Final Heaven
  (`1100 2000 4000 8000 0010`) is a full d-pad rotation followed by Triangle. Note the engine
  remaps ids 128-139 through the player's **key config** at runtime, so the glyph a player sees
  depends on their bindings; icon.sp1 ships the PlayStation pad set.
* **Angelo move (0x1B)** — ORs `1 << id` into `SG_ANGELO_KNOWN`, and draws nothing. The Pet Pals
  pages show their dog through an ordinary picture overlay like any other page.

## Function addresses

| Function | Address   | Description                                                  |
|-----------|-----------------------------------|--------------------------------------------------------------|
| `Menu_Magazine_Update` | 0x4C9060  | Viewer state machine (page turning, zoom)                    |
| `Menu_Magazine_Draw` | 0x4C9330  | Draws window, page picture, text overlays, footer            |
| `Menu_Magazine_DrawPictureOverlays` | 0x4C9670  | Draws the 4 picture overlay slots                            |
| `Menu_Magazine_DrawPageImage` | 0x4C95A0  | Draws the paper mat rectangle                                |
| `Menu_ItemMagazine_DrawPageImage` | 0x4FDA50 | The item reader's copy of it, same logic                  |
| `menu_draw_text` | 0x4BDE30  | Glyph blitter: cell = code - 0x20, atlas of 21 columns of 12x12, +13 y per line break |
| `menu_draw_number_rightaligned` | 0x4A3400 | Draws a number ending on the given x (via `menu_draw_number_colorsel`, 0x4A3530) |
| `getTextBattleItem` | 0x47EA30  | Item name, from the kernel's item name text sections        |
| `Menu_Magazine_LoadPageTexture` | 0x4C9920  | Loads the page picture TIM from category/page                |
| `Menu_Magazine_DrawPaperBackground` | 0x4C96F0  | Draws the paper background in 64-pixel strips                |
| `Menu_ItemMagazine_DrawPaperBackground` | 0x4FD5B0 | The item reader's copy of it, same logic                |
| `Menu_LoadMngrpTextureAsync` | 0x4AC400  | Loads a mngrp raw file and uploads its TIM to the emulated VRAM at the header-declared placement (page pictures, parchment raw 12) |
| `Menu_Tutorial_Update` | 0x4C9CB0  | Tutorial menu state machine; case 14 uploads raw 7 (sprites) + raw 12 (parchment) on book open |
| `Menu_Magazine_FirstEntry` | 0x1D7D3A5 | First mmag entry of the currently open book                  |
| `Menu_Magazine_LastEntry` | 0x1D7D3A6 | Last mmag entry of the currently open book                   |
| `Menu_DrawSp2Sprite` | 0x4FDCA0  | Generic SP2 quad-list sprite renderer (also cardanm.sp2)     |
| `Menu_ItemMagazine_Draw` | 0x4FC990  | Item-menu reader main draw (parallel implementation)         |
| `Menu_ItemMagazine_DrawPage` | 0x4FD6E0  | Item-menu page draw, incl. the unlock fields 0x18-0x22       |
| `Menu_BookTextBuffer` | 0x1D773A4 | Static buffer receiving the book-text string section         |
| `mmagbinbuffer` | 0x1D2BAF8 | Pointer to the loaded mmag.bin                               |
| `mmagbuffer` | 0x1D2BB6C | Second in-memory copy of mmag.bin used by the item-menu reader |
