---
title: Section 9 - Sounds
layout: default
parent: Monster files (c0mxxx.dat)
permalink: /technical-reference/battle/monster-files-c0mxxxdat/section-9-sounds/
nav_order: 9
---

## Section 9: Sounds

Contains AKAO sequences (can be empty).

| Offset           | Length             | Description      |
|------------------|--------------------|--------------------|
| 0                | 2 bytes            | Number of AKAOs  |
| 2                | nbAKAOs \* 2 bytes | AKAOs Positions  |
| 2 + nbAKAOs \* 2 | 2 bytes            | End of section 9 |
| 4 + nbAKAOs \* 2 | Varies \* nbAKAOs  | AKAOs            |
