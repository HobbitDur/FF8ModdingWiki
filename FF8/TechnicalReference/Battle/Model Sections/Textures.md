---
title: Textures
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/textures/
nav_order: 11
author: HobbitDur
---

## Textures

Holds the monster's texture pages as standard PlayStation [TIMs]({{site.baseurl}}/technical-reference/psx/tim-file-format).

| Offset          | Length            | Description                |
|-----------------|-------------------|----------------------------|
| 0               | 4 bytes           | Number of TIMs             |
| 4               | nbTIMs \* 4 bytes | TIMs Positions             |
| 4 + nbTIMs \* 4 | 4 bytes           | End offset (= section size)|
| 8 + nbTIMs \* 4 | Varies \* nbTIMs  | TIMs                       |

Positions and the trailing End offset are byte offsets from the start of the section (the End offset equals the section length, giving the size of the last TIM). Each pointed block is a complete TIM, with its own header declaring the pixel-data VRAM destination, colour depth (4-bit or 8-bit CLUT) and the palette(s) it carries.

Most monsters ship a single TIM; larger or multi-part enemies use several. Together the TIMs make up the monster's texture pages in VRAM, and the model primitives in [model geometry](../model-geometry/) address them through their `textureID_related` (CLUT selector) and `textureID_related2` (texture-page / TPage) fields — so a primitive's on-screen appearance comes from pairing its TPage/CLUT with the pixels and palettes uploaded from this section.

The [dynamic texture data](../dynamic-texture-data/) works on the same uploaded texture pages, copying/scrolling sub-regions of them at runtime (blink-eyes, conveyor effects…).
