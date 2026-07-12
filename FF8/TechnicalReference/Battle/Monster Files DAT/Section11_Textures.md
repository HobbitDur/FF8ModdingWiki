---
title: Section 11 - Textures
layout: default
parent: Monster files (c0mxxx.dat)
permalink: /technical-reference/battle/monster-files-c0mxxxdat/section-11-textures/
nav_order: 11
---

## Section 11: Textures

Contains some [TIMs]({{site.baseurl}}/technical-reference/psx/tim-file-format).

| Offset          | Length            | Description    |
|-----------------|-------------------|-----------------|
| 0               | 4 bytes           | Number of TIMs |
| 4               | nbTIMs \* 4 bytes | TIMs Positions |
| 4 + nbTIMs \* 4 | 4 bytes           | End of file    |
| 8 + nbTIMs \* 4 | Varies \* nbTIMs  | TIMs           |
