---
title: Dynamic texture data
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/dynamic-texture-data/
nav_order: 4
author: HobbitDur
---

## Dynamic texture data

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
  BYTE anim_speed;                      ///< Playback speed (see below); 0 = scroll mode
  BYTE frame_counter;                   ///< Runtime accumulator, always 0 in the file
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

### Playback (`anim_speed` / `frame_counter`)

The animation is advanced by [animation sequences](../animation-sequences/) opcode `80`. Only `anim_speed` comes from the file; `frame_counter` is runtime state (0 on disk):

- **`anim_speed` == 0** — *scroll mode*: the copied VRAM region is scrolled rather than frame-swapped. (`number_destination` is 0 in this case.)
- **`anim_speed` == 8** — one destination frame is shown per tick; `frame_counter` cycles `0 .. number_destination`.
- **any other value** — `anim_speed` is a speed in **1/8-frame units**: each tick adds it to `frame_counter` (which runs `0 .. 8*(number_destination+1)`), and the visible frame is `frame_counter / 8`. So smaller values play slower, `8` is one frame per tick.

TODO: Add the monster list that have an animated texture section.
