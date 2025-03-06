---
layout: default
title: Header
nav_order: 1
parent: Kernel
slug: header
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x0000 | 1        | 228 bytes    |

## Section Structure

| Offset | Length  | Description                                                                                                       |
|--------|---------|-------------------------------------------------------------------------------------------------------------------|
| 0x0000 | 4 bytes | Number of sections                                                                                                |
| 0x0004 | 4 bytes | Offset to [**Battle commands** section                              ](../Battle-commands)                         |
| 0x0008 | 4 bytes | Offset to [**Magic data** section                                   ](../Magic)                                   |
| 0x000C | 4 bytes | Offset to [**Junctionable GFs** section                             ](../Junctionable-GFs)                        |
| 0x0010 | 4 bytes | Offset to [**Enemy attacks** section                                ](../Enemy-attacks)                           |
| 0x0014 | 4 bytes | Offset to [**Weapons** section                                      ](../Weapons)                                 |
| 0x0018 | 4 bytes | Offset to [**Renzokuken finishers** section                         ](../Renzokuken-finishers)                    |
| 0x001C | 4 bytes | Offset to [**Characters** section                                   ](../Characters)                              |
| 0x0020 | 4 bytes | Offset to [**Battle items** section                                 ](../Battle-items)                            |
| 0x0024 | 4 bytes | Offset to [**Non-battle item name and description offsets** section ](../Non-battle-item-and-description-offsets) |
| 0x0028 | 4 bytes | Offset to [**Non-junctionable GF attacks** section                  ](../Non-junctionable-GF-attacks)             |
| 0x002C | 4 bytes | Offset to [**Command abilities in battle** section                  ](../Command-abilities-in-battle)             |
| 0x0030 | 4 bytes | Offset to [**Junction abilities** section                           ](../Junction-abilities)                      |
| 0x0034 | 4 bytes | Offset to [**Command abilities GF** section                         ](../Command-abilities-gf)                    |
| 0x0038 | 4 bytes | Offset to [**Stat percentage increasing abilities** section         ](../Stat-percentage-increasin-abilities)     |
| 0x003C | 4 bytes | Offset to [**Character abilities** section                          ](../Character-abilities)                     |
| 0x0040 | 4 bytes | Offset to [**Party abilities** section                              ](../Party-abilities)                         |
| 0x0044 | 4 bytes | Offset to [**GF abilities** section                                 ](../GF-abilities)                            |
| 0x0048 | 4 bytes | Offset to [**Menu abilities** section                               ](../Menu-abilities)                          |
| 0x004C | 4 bytes | Offset to [**Temporary character limit breaks** section             ](../Temporary-character-limit-breaks)        |
| 0x0050 | 4 bytes | Offset to [**Blue magic (Quistis limit break)** section             ](../Blue-magic)                              |
| 0x0054 | 4 bytes | Offset to [**Blue magic Parameters** section                        ](../Blue-magic-parameters)                   |
| 0x0058 | 4 bytes | Offset to [**Shot (Irvine limit break)** section                    ](../Shot-(irvine-limit-breaks))              |
| 0x005C | 4 bytes | Offset to [**Duel (Zell limit break)** section                      ](../Duel-(zell-limit-breaks))                |
| 0x0060 | 4 bytes | Offset to [**Duel Params** section                                  ](../Duel-params)                             |
| 0x0064 | 4 bytes | Offset to [**Rinoa limit breaks (part 1)** section                  ](../Rinoa-commands)                          |
| 0x0068 | 4 bytes | Offset to [**Rinoa limit breaks (part 2)** section                  ](../Rinoa-combine-limit-break)               |
| 0x006C | 4 bytes | Offset to [**Slots Array** section                                  ](../Slots-array)                             |
| 0x0070 | 4 bytes | Offset to [**Slots Sets** section                                   ](../Slots-seets)                             |
| 0x0074 | 4 bytes | Offset to [**Devour** section                                       ](../Devour)                                  |
| 0x0078 | 4 bytes | Offset to [**Misc** section                                         ](../Misc)                                    |
| 0x007C | 4 bytes | Offset to [**Misc text pointers** section                           ](../Misc-text-pointers)                      |
| 0x0080 | 4 bytes | Offset to **Battle command text** section                                                                         |
| 0x0084 | 4 bytes | Offset to **Magic text** section                                                                                  |
| 0x0088 | 4 bytes | Offset to **Junctionable GF text** section                                                                        |
| 0x008C | 4 bytes | Offset to **Enemy attack text** section                                                                           |
| 0x0090 | 4 bytes | Offset to **Weapon text** section                                                                                 |
| 0x0094 | 4 bytes | Offset to **Renzokuken finishers text** section                                                                   |
| 0x0098 | 4 bytes | Offset to **Character names** section                                                                             |
| 0x009C | 4 bytes | Offset to **Battle item names** section                                                                           |
| 0x00A0 | 4 bytes | Offset to **Non-battle item names** section                                                                       |
| 0x00A4 | 4 bytes | Offset to **Non-junctionable GF attack name** section                                                             |
| 0x00A8 | 4 bytes | Offset to **Junction abilities text** section                                                                     |
| 0x00AC | 4 bytes | Offset to **Command abilities text** section                                                                      |
| 0x00B0 | 4 bytes | Offset to **Stat percentage increasing abilities text** section                                                   |
| 0x00B4 | 4 bytes | Offset to **Character ability text** section                                                                      |
| 0x00B8 | 4 bytes | Offset to **Party ability text** section                                                                          |
| 0x00BC | 4 bytes | Offset to **GF ability text** section                                                                             |
| 0x00C0 | 4 bytes | Offset to **Menu ability text** section                                                                           |
| 0x00C4 | 4 bytes | Offset to **Temporary character limit break text** section                                                        |
| 0x00C8 | 4 bytes | Offset to **Blue magic text** section                                                                             |
| 0x00CC | 4 bytes | Offset to **Shot text** section                                                                                   |
| 0x00D0 | 4 bytes | Offset to **Duel text** section                                                                                   |
| 0x00D4 | 4 bytes | Offset to **Rinoa limit break (part 1) text** section                                                             |
| 0x00D8 | 4 bytes | Offset to **Rinoa limit break (part 2) text** section                                                             |
| 0x00DC | 4 bytes | Offset to **Devour text** section                                                                                 |
| 0x00E0 | 4 bytes | Offset to **Misc text** section                                                                                   |
