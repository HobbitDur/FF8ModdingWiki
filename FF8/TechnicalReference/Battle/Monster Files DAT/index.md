---
title: Monster files (c0mxxx.dat)
layout: default
parent: Battle
author: Mirex, JWP, random_npc, myst6re, HobbitDur
permalink: /technical-reference/battle/monster-files-c0mxxxdat/
nav_order: 1
---

1. TOC
{:toc}

## Header

DAT file is divided into 11 sections (except for c0m127.dat, which contains only 2 sections : 7th and 8th).

| Offset              | Length                | Description                                            |
|---------------------|-----------------------|--------------------------------------------------------|
| 0                   | 4 bytes               | Number of sections (always =11, except for c0m127.dat) |
| 4                   | nbSections \* 4 bytes | Section Positions                                      |
| 4 + nbSections \* 4 | 4 bytes               | File size                                              |

## Sections

- [Section 1: Skeleton](section-1-skeleton/)
- [Section 2: Model geometry](section-2-model-geometry/)
- [Section 3: Model animation](section-3-model-animation/)
- [Section 4: Dynamic texture data](section-4-dynamic-texture-data/)
- [Section 5: Animation sequences](section-5-animation-sequences/)
- [Section 6: Camera sequence](section-6-camera-sequence/)
- [Section 7: Informations & stats](section-7-informations-stats/)
- [Section 8: Battle scripts/AI](section-8-battle-scripts-ai/)
- [Section 9: Sounds](section-9-sounds/)
- [Section 10: Sounds/Unknown](section-10-sounds-unknown/)
- [Section 11: Textures](section-11-textures/)
- [Other c0mxxx.dat-like files (dXcYYY.dat, dXwYYY.dat)](other-dat-files/)
