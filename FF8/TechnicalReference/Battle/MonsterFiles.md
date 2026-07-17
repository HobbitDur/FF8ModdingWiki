---
title: Monster files (c0mxxx.dat)
layout: default
parent: Battle
author: Mirex, JWP, random_npc, myst6re, HobbitDur
permalink: /technical-reference/battle/monster-file/
nav_order: 2
---

1. TOC
{:toc}

A monster file carries all 11 [model building-block sections](../model-sections/). The
same blocks (with a different numbering) make up the playable [character & weapon
files](../character-weapon-files/) — see [Model file sections](../model-sections/)
for the shared formats.

## Header

DAT file is divided into 11 sections (except for c0m127.dat, which contains only 2 sections : 7th and 8th).

| Offset              | Length                | Description                                            |
|---------------------|-----------------------|--------------------------------------------------------|
| 0                   | 4 bytes               | Number of sections (always =11, except for c0m127.dat) |
| 4                   | nbSections \* 4 bytes | Section Positions                                      |
| 4 + nbSections \* 4 | 4 bytes               | End offset (= file size)                               |

Section Positions and the trailing End offset are byte offsets from the start of the file. The End offset is one-past the last section, so it equals the file size and also gives the length of the last section: `len(section i) = position[i+1] - position[i]`, with the End offset acting as `position[nbSections]`.

## Sections

| # | Section ([format](../model-sections/))                    |
|---|-----------------------------------------------------------|
| 1 | [Skeleton](../model-sections/skeleton/)                   |
| 2 | [Model geometry](../model-sections/model-geometry/)      |
| 3 | [Model animation](../model-sections/model-animation/)    |
| 4 | [Dynamic texture data](../model-sections/dynamic-texture-data/) |
| 5 | [Animation sequences](../model-sections/animation-sequences/) |
| 6 | [Camera sequence](../model-sections/camera-sequence/)    |
| 7 | [Information & stats](../model-sections/information-stats/) |
| 8 | [Battle scripts / AI](../model-sections/battle-scripts-ai/) |
| 9 | [Sounds](../model-sections/sounds/)                       |
| 10 | [Sound sample bank](../model-sections/sound-sample-bank/) |
| 11 | [Textures](../model-sections/textures/)                  |

(`c0m127.dat` is the exception: it holds only sections 7 and 8.)
