---
layout: default
parent: Menu
title: Menu sprite tables (.sp1 / .sp2 file formats)
permalink: /technical-reference/menu/sp1-sp2/
author: hobbitdur
---

The menu module describes its UI sprites (icons, portraits, card animations, magazine pictures) with two small
quad-list formats. Both map sprite ids to lists of textured quads; they differ in directory layout and quad
size. The texture itself lives elsewhere (a TIM already uploaded to VRAM) — these files only carry UV/CLUT
rectangles and draw offsets.

## .sp1 format (icon.sp1)

| Offset | Size | Description                                                              |
|--------|------|--------------------------------------------------------------------------|
| 0x00   | 4    | UInt32 icon count (329 in icon.sp1)                                     |
| 0x04   | 4×N  | Directory, one UInt32 per icon id: {UInt16 offset from file start, UInt16 quad count} |
| ...    | -    | Quads (8 bytes each)                                                     |

Each quad is 8 bytes, two packed UInt32:

* **DWord 0**: bits 0-15 = texture UV (byte U, byte V) · bits 16-26 = CLUT selector (the primitive CLUT is
  0x3810 + these bits) · bit 27 = semi-transparency (ABE) · bits 30-31 = texture page (E1 bits 5-6).
* **DWord 1**: byte 0 = width · byte 1 = signed X offset · byte 2 = height · byte 3 = signed Y offset.

Icon ids **128-139** are not read from the file: they are the confirm/cancel/etc. button icons, redirected to
a dedicated renderer that remaps them through the controller key configuration.

The text engine draws icons with control code `0x05 NN` (see
[MenuModuleRuntime](../menu-module-runtime/)), but `NN` is **not** the icon id directly.
`Text_RenderGlyphs` resolves it as:

| `NN` | Icon id drawn |
|------|---------------|
| `0x20`–`0x2F` | controller button icon, through the key configuration |
| `0x30`–`0x3F` | `NN + 80` |
| `0x40`–`0x7E` | `TEXT_ICON_CODE_TO_SPRITE[NN]`, a table of 16-bit ids at `0xB86D84` (EN 2013) |

The table's entries include the status icons (`0x53`–`0x59`, `0x65`–`0x71` → ids `0x110`–`0x11C`)
and the eight element icons (`0x5D`–`0x64` → ids `0x120`–`0x127`, the "names" kernel misc text
101–108 hold). It ends at `0x7E`; see [Element System]({{site.baseurl}}/technical-reference/battle/element-system/#element-names-are-icon-tokens-not-words)
for the full list.

Two different renderers read this file, and only one is bounds-checked. `Menu_DrawSp1SpriteById`
(`0x4B7210`, used by the menu pages) returns without drawing when the id is at or past the
file's icon count. The text path — `Menu_DrawSp1Icon` (`0x4B75B0`) and
`Menu_GetSp1IconSize` (`0x4B73F0`) — does not check, so a text icon code that resolves past the
end of the file reads beyond the directory.

`icon.sp1` is loaded by `Menu_LoadFile` into an allocation of the file's own size, so sprites
can be appended: add a directory entry, move every existing offset by 4, and put the new quads
at the end.

## .sp2 format (face.sp2, cardanm.sp2, mngrp Pos 4)

| Offset | Size | Description                                                              |
|--------|------|--------------------------------------------------------------------------|
| 0x00   | 4    | UInt32 sprite count                                                      |
| 0x04   | 4×N  | UInt32 offsets from file start, one per sprite id (0 = unused id)        |
| ...    | -    | Sprite records                                                           |

Each sprite record is a UInt32 quad count followed by 12 bytes per quad:

| Offset | Size | Description                                   |
|--------|------|---------------------------------------------------|
| 0x00   | 1    | Texture U                                         |
| 0x01   | 1    | Texture V                                         |
| 0x02   | 2    | CLUT id                                           |
| 0x04   | 2    | Width                                             |
| 0x06   | 2    | Height                                            |
| 0x08   | 1    | Signed X offset from the sprite draw position     |
| 0x09   | 1    | Signed Y offset                                   |
| 0x0A   | 2    | Texture page (PS1 GPU E1 bits, masked with 0x9FF) |

## Known files

| File          | Sprites | Content                                                   |
|---------------|---------|---------------------------------------------------------------|
| icon.sp1      | 329     | UI icons (element/status symbols, cursors, button icons...)   |
| face.sp2      | 64      | Character and GF portraits (32×48)                            |
| cardanm.sp2   | 12      | Triple Triad card flip animation frames (64×64)               |
| [mngrp.bin](../mngrpbin-file-format/) Pos 4 | 79 (39 used) | Magazine and Chocobo World screen pictures    |

## Addresses (FF8 PC 2000 EN)

| Address  | Name                | Description                              |
|----------|---------------------|----------------------------------------------|
| 0x4B75B0 | Menu_DrawSp1Icon    | SP1 icon renderer                            |
| 0x4B73F0 | Menu_GetSp1IconSize | Bounding box (max width/height incl. offsets) |
| 0x4FDCA0 | Menu_DrawSp2Sprite  | Generic SP2 sprite renderer                  |
