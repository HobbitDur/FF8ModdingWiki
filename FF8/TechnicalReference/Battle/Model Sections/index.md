---
title: Model file sections
layout: default
parent: Battle
permalink: /technical-reference/battle/model-sections/
nav_order: 1
author: HobbitDur
---

1. TOC
{:toc}

## Battle model sections

Every battle model in `battle.fs` — monsters (`c0mxxx.dat`), playable
**characters** (`dXcYYY.dat`) and their **weapons** (`dXwYYY.dat`) — is built from
the **same container** (a section count, a table of per-section byte offsets, and
a trailing end offset equal to the file size) filled with a selection of the same
**section building blocks**.

These pages document each building block once, independently of the file it
appears in. The file-type pages then list which blocks they use and in what
order:

- [Monster files (c0mxxx.dat)](../monster-files-c0mxxxdat/) — all 11 blocks.
- [Character & weapon files (dXcYYY.dat / dXwYYY.dat)](../character-weapon-files/) — a subset each.

Because the section *number* depends on the file type (the camera block is
monster section 6 but character section 5, for example), the numbering lives on
those file-type pages; the blocks below are referenced by name.

## The building blocks

| Building block                                        | Purpose                                                              |
|-------------------------------------------------------|---------------------------------------------------------------------|
| [Skeleton](skeleton/)                                 | Bone hierarchy and rest pose.                                        |
| [Model geometry](model-geometry/)                     | The mesh — objects, vertices and primitive lists.                   |
| [Model animation](model-animation/)                   | Key-framed bone animation pool.                                     |
| [Dynamic texture data](dynamic-texture-data/)         | Runtime VRAM sub-region copy/scroll (blink-eyes, conveyor…).        |
| [Animation sequences](animation-sequences/)           | Byte-code VM that decides which animation plays for each action.    |
| [Camera sequence](camera-sequence/)                   | Byte-code VM (same engine) driving key-framed camera motion.        |
| [Information & stats](information-stats/)             | Combat stats, elemental/status affinities, rewards, AI flags.       |
| [Battle scripts / AI](battle-scripts-ai/)             | The enemy AI script program.                                        |
| [Sounds](sounds/)                                     | AKAO sound-effect sequences.                                        |
| [Sound sample bank](sound-sample-bank/)               | AKAO ADPCM sample bank (vestigial on PC).                           |
| [Textures](textures/)                                 | PlayStation TIM texture pages.                                      |
