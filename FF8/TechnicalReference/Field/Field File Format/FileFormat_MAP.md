---
layout: default
parent: Field File Format
title: Field Background Tile Data
permalink: /technical-reference/field/field-file-format/field-background-tile-data/
---

By Aali.

# MAP Files

MAP files contain data about the tiles used to draw the field background. There is no header, every 16 bytes of the file is one 16x16 tile from the MIM data, ending with the special signature 0x7FFF followed by 12 zero bytes. To determine whether you're dealing with a type 1 or type 2 file, look at the MIM filesize, there is no obvious marker for type 2 in the MAP file.

## Tile format

### Type 1

Two signed 16-bit integers, X and Y relative to center (0, 0)  
Unsigned 16-bit Z: the tile's draw depth, see [Z: draw depth](#z-draw-depth) below  
4 bits, which 128x256 texture to use, if you consider the MIM to be one big image, just multiply this value by 128 and add it to the source X coordinate  
1 unknown bit, always 1 (except in ending.map)  
1 bit, image depth. 0 - there is two color indexes per byte (4-bit indexed), 1 there is one color index per byte (8-bit indexed)
2 unknown bits, seem to be always equal to (blend mode % 4), except in some test fields
1 Unknown byte, always 0 (except in ending.map)  
6 unknown bits, always 0  
4 bits specifying which palette to use, add 8 to this number to get the right palette from the MIM  
6 unknown bits, always 15  
2 bytes, source X and Y coordinates to sample the tile from  
1 bit, always 0  
7 bits, layer id  
1 byte specifying which blend mode to use for this tile, 1 is additive blending, 2 is subtractive blending, 3 seems to be +25%, 4 seems to be the default (no blending) and 0 is unknown (elview1)  
1 byte, background animation id  
1 byte, animation state  

### Type 2

X and Y, same as above  
Source coordinates, both 16-bit this time  
Z, same as above  
4 bits, which 128x256 texture to use, same as above  
4 unknown bits (maybe same as above)  
1 unknown byte, always 0  
6 unknown bits, always 0  
4 bits specifying which palette to use, add 8 to this number to get the right palette from the MIM  
6 unknown bits, always 15  
1 byte, background animation id  
1 byte, animation state  

## Z: draw depth

A field background is a flat picture, but characters must be able to walk behind parts of it (a pillar, a lamp post). The tile Z is what makes this work: it is the tile's **distance from the camera divided by 4**, on the same scale the game uses to sort the 3D models.

Every frame the field module fills one ordering table of 4096 slots (the PlayStation way of sorting what to draw) and draws it from slot 4095 down to slot 0, so a higher slot is drawn first and ends up behind:

| What | Slot | Function (FF8_EN.exe) |
|---|---|---|
| Background tile | its Z | `Field_BG_BuildTileDrawList` (0x475480) |
| Character model triangle or quad | depth from the camera of its first vertex / 4 (one slot further than shadows) | `Field_Chara_InsertModelTrianglesByDepth` (0x533920), `Field_Chara_InsertModelQuadsByDepth` (0x533A90) |
| Character shadow | depth from the camera of its last point / 4 | `Field_Chara_DrawCircleShadows` (0x472F20) |

The depth is the camera-space Z computed by the GTE projection (`GTE_RTPT`), in walkmesh units, with the camera of the `.ca` file. So a character further from the camera than 4 × Z is covered by the tile, and a nearer one is drawn over it. Model polygons nearer than 30 or at 0x4000 and beyond are not drawn. Within a slot, tiles are ordered by 16 × Z plus the order their palette first appears.

In practice:

* **Base picture:** almost every tile (floor, walls, sky) has Z = 4094, behind everything.
* **Foreground pieces:** only the tiles a character can pass behind get a smaller Z, the depth of that object. In bgroad_6, 698 tiles are at 4094 and the 50 tiles of the pillars at 1528 (6112 units from the camera). Across the 895 retail fields the median is 8 different Z values per field, and 131 fields have only 1 or 2.
* **Check:** in bcgate1a, bgroad_6, glpreo2 and bccent_1, 4 × Z of the foreground tiles lies inside the range of distances from the camera of the field's own walkmesh.

This also means Z cannot rebuild the scenery in 3D: the base picture carries no depth at all, only the foreground pieces do, one value per tile.
