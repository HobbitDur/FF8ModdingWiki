---
title: Section 8 - Battle scripts/AI
layout: default
parent: Monster files (c0mxxx.dat)
permalink: /technical-reference/battle/monster-files-c0mxxxdat/section-8-battle-scripts-ai/
nav_order: 8
---

## Section 8: Battle scripts/AI

| Offset | Length  | Description                |
|--------|---------|-----------------------------|
| 0      | 4 bytes | Number of sub-sections     |
| 4      | 4 bytes | Offset to AI sub-section   |
| 8      | 4 bytes | Offset to text offsets     |
| 12     | 4 bytes | Offset to text sub-section |

### AI

| Offset | Length  | Description                              |
|--------|---------|--------------------------------------------|
| 0      | 4 bytes | Offset to init code                      |
| 4      | 4 bytes | Offset to code executed at ennemy's turn |
| 8      | 4 bytes | Offset to counterattack code             |
| 12     | 4 bytes | Offset to death code                     |
| 16     | 4 bytes | Offset to "before dying or taking a hit" |

The runtime interpreter and section dispatch are documented in [Enemy AI VM Runtime](../../enemy-ai-vm-runtime/). The per-opcode authoring reference
is [Battle Scripts](../../battle-scripts/).

### Texts

Text offsets is a list of text positions (2 bytes each) in the text sub-section.
