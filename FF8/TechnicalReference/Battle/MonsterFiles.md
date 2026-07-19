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

DAT file is divided into 11 sections (except for c0m127.dat, which contains only 2 sections: info & stats, then battle scripts / AI).

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
| 6 | [Camera sequence](../model-sections/camera-sequence/) — a **bare** [camera animation collection](../file-format-x/#camera-animations-collection) (no blob header, no byte-code; see the [container-forms note](../model-sections/camera-sequence/#two-container-forms-important)) |
| 7 | [Information & stats](../model-sections/information-stats/) |
| 8 | [Battle scripts / AI](../model-sections/battle-scripts-ai/) |
| 9 | [Sounds](../model-sections/sounds/)                       |
| 10 | [Sound sample bank](../model-sections/sound-sample-bank/) |
| 11 | [Textures](../model-sections/textures/)                  |

### The no-model exception: c0m127.dat

`c0m127.dat` (com_id 127 = "Ultimecia (No Model, has Apocalypse)", per the internal enemy list) is the one file that doesn't follow the 11-section layout. It's an invisible, untargetable trigger entity used purely to cast the Apocalypse attack in the final battle — it has no skeleton, geometry, animation, dynamic texture, camera, animation-sequence, sound, or texture section at all, just enough to define its stats and its AI script.

Header: `Number of sections = 2` (raw field; +1 convention gives 3 total slots including the header itself), so the position table is only 3 entries (16, 396, 460 bytes on the shipped file — a 460-byte file in total). The two real sections use the *same formats* as a normal monster's sections 7 and 8, just renumbered to 1 and 2 since there's nothing before them:

| # | Section ([format](../model-sections/)) | Notes |
|---|---|---|
| 1 | [Information & stats](../model-sections/information-stats/) | 380 bytes — identical size and layout to a normal monster's section 7. `monster_name` decodes to `"Ultimecia"`; the `Hidden HP` and `Fly` flags are set. |
| 2 | [Battle scripts / AI](../model-sections/battle-scripts-ai/) | Identical layout to a normal monster's section 8. Decompiles to coherent code: `untargetable();` on init, `untargetable(); vanish();` on death, and no-ops (`stop();`) on its turn and on counterattack — consistent with an invisible entity that never acts and can't be targeted. |

[FF8UltimateEditor](https://github.com/HobbitDur/FF8UltimateEditor)'s Ifrit tool recognizes this layout as `EntityType.MONSTER_NO_MODEL` (detected purely from the section count in the header, like every other entity type) and exposes it through the normal **Stat** and **AI** tabs — every other tab (3D, Sequence, Camera, Dynamic Texture, Static Texture) is hidden, since none of those sections exist on this file.
