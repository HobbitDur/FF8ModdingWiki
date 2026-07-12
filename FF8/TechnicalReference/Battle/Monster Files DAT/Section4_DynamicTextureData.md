---
title: Section 4 - Dynamic texture data
layout: default
parent: Monster files (c0mxxx.dat)
permalink: /technical-reference/battle/monster-files-c0mxxxdat/section-4-dynamic-texture-data/
nav_order: 4
---

## Section 4: Dynamic texture data

Optional section, often empty.
It contains info on dynamic texture (like blink-eyes)

It starts with a list of offset followed by data.
The offset list start with a 0 offset which must be ignored. Each offset is 2 bytes.
The number of offset need to be deduced: so read each 2 bytes till you read a bit that is inferior to the previous.
The offset value start at the beginning of the section.

Each data pointed by the offset look like this:

```
struct DynamicTextureData
{
  BYTE textureNum;                      ///< Which texture page/slot to use
  BYTE vram_x_offset;
  BYTE vram_y_offset;
  BYTE sprite_width_in_vram_coord;      ///< Width of region to copy, in X you need to multiply by 2 to get the pixel value
  BYTE sprite_height_in_vram_coord;     ///< Height of region to copy
  BYTE number_destination;
  WORD unk2;
  BYTE source_uv_u;                     ///< X offset of source sprite in VRAM (x2 to get pixel for X)
  BYTE source_uv_v;                     ///< Y offset of source sprite in VRAM
  UV_VRAM dest_uv[6]; ///< Actually pairs of bytes: {dest_u, dest_v} for each frame
};
struct UV_VRAM
{
  BYTE u;                               ///< X in VRAM (x2 to get pixel)
  BYTE v;                               ///< Y in VRAM
};

```

The number of `dest_uv` depends of the `number_of_destination`.

Important point is that all UV and sprite width/height is expressed in VRAM value, which mean you need to multiply the X value by 2 to get the pixel value (Y is
already in pixel).

TODO: Add the monster list that have an animated texture section.
