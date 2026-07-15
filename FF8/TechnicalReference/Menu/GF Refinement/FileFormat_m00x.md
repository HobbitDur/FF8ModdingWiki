---
layout: default
parent: GF Refinement
title: Refine abilities
permalink: /technical-reference/menu/gf-refinement/refine-abilities/
---


# General

m00x files manages the refine abilities of gforce that transform object/card into whatever.

The bin files contains the offset to string and all useful values.

The msg files contains only text that is shown to the user when refining. The text is not link to the items, so you
could transform one card to a potion, the text could be "Let's have fun on my switch tonight".

It is important to note that the original files  (m00x.bin and m00x.msg) are actually not used by the game,
but only the one contains in the [mngrp.bin](https://github.com/HobbitDur/ShumiTranslator/wiki/Mngrp_bin) file.

The [mngrphd.bin](https://github.com/HobbitDur/ShumiTranslator/wiki/Mngrphd_bin) contains offset for mngrp and is different for every language.

At runtime, the refine menu (`Menu_Prog19_RefineMenu_Init`) loads the mngrp copies by raw
mngrphd entry index: entries **188-192** for m000.bin-m004.bin (into the buffer at 0x1D8A864) and entries
**196-200** for m000.msg-m004.msg (into 0x1D85864). The 8-byte entry stride is confirmed by the executable.

# BIN

There is 5 bin files:

* m000.bin
* m001.bin
* m002.bin
* m003.bin
* m004.bin

m00x.bin files contains offsets of [strings](#msg) and actual values for Refine Abilities.
Each m00x file has a specific number of entries, which are listed here.

## m000.bin

### Data

8 abilities

| Ability                                     | \# of Entries | mngrp.bin Location        | Offset | Description                |
|---------------------------------------------|---------------|---------------------------|--------|----------------------------|
| [[T Mag-RF\|Refinement#t-mag-rf]]           | 7 entries     | (mngrp.bin loc: 0x21F000) | 0x0    | Item to Thunder/Wind Magic |
| [[I Mag-RF\|Refinement#i-mag-rf]]           | 7 entries     | (mngrp.bin loc: 0x21F038) | 0x38   | Item to Ice/Water Magic    |
| [[F Mag-RF\|Refinement#f-mag-rf]]           | 10 entries    | (mngrp.bin loc: 0x21F070) | 0x70   | Item to Fire/Flare Magic   |
| [[L Mag-RF\|Refinement#L-mag-rf]]           | 21 entries    | (mngrp.bin loc: 0x21F0C0) | 0xC0   | Item to Life Magic         |
| [[Time Mag-RF\|Refinement#time-mag-rf]]     | 14 entries    | (mngrp.bin loc: 0x21F168) | 0x168  | Item to Time Magic         |
| [[ST Mag-RF\|Refinement#st-mag-rf]]         | 17 entries    | (mngrp.bin loc: 0x21F1D8) | 0x1D8  | Item to Status Magic       |
| [[Supt Mag-RF\|Refinement#supt-mag-rf]]     | 20 entries    | (mngrp.bin loc: 0x21F260) | 0x260  | Items to Support Magic     |
| [[Forbid Mag-RF\|Refinement#forbid-mag-rf]] | 6 entries     | (mngrp.bin loc: 0x21F300) | 0x300  | Items to Forbidden Magic   |

### Entry

8 bytes

| Type   | Size | Value                                                                          | Description                              |
|--------|------|--------------------------------------------------------------------------------|------------------------------------------|
| UInt16 | 2    | Offset                                                                         | Offset to the string                     
| Byte   | 1    | Received                                                                       | Amount received                          |
| UInt16 | 2    | UNK                                                                            | {0x0001}                                 |
| Byte   | 1    | [Input\_Item\_ID](https://github.com/HobbitDur/FF8GameData/wiki#item-list)     | Input: Item id value **0x00**-**0xC6**   |
| Byte   | 1    | Required                                                                       | Amount needed                            |
| Byte   | 1    | [Output\_Spell\_ID](https://github.com/HobbitDur/FF8GameData/wiki#magic-items) | Output: Spell id value **0x01**-**0x38** |

## m001.bin

### Data

7 abilities

| Ability                                       | \# of Entries | mngrp.bin Location        | Offset | Description                       |
|-----------------------------------------------|---------------|---------------------------|--------|-----------------------------------|
| [[Recov Med-RF\|Refinement#recov-med-rf]]     | 9 Entries     | (mngrp.bin loc: 0x21F800) | 0x0    | Item to Recovery Items            |
| [[ST Med-RF\|Refinement#st-med-rf]]           | 12 Entries    | (mngrp.bin loc: 0x21F848) | 0x48   | Item to Status Removal Items      |
| [[Ammo-RF\|Refinement#ammo-rf]]               | 16 Entries    | (mngrp.bin loc: 0x21F8A8) | 0xA8   | Item to Ammo Item                 |
| [[Forbid Med-RF\|Refinement#forbid-med-rf]]   | 20 Entries    | (mngrp.bin loc: 0x21F928) | 0x128  | Item to Forbidden Medicine        |
| [[GFRecov Med-RF\|Refinement#gfrecov-med-rf]] | 12 Entries    | (mngrp.bin loc: 0x21F9C8) | 0x1C8  | Item to GF Recovery Items         |
| [[GFAbl Med-RF\|Refinement#gfabl-med-rf]]     | 42 Entries    | (mngrp.bin loc: 0x21FA28) | 0x228  | Item to GF Ability Medicine Items |
| [[Tool-RF\|Refinement#tool-rf]]               | 32 Entries    | (mngrp.bin loc: 0x21FB78) | 0x378  | Item to Tool Items                |

### Entry

8 bytes

| Type   | Size | Value                                                                       | Description                             |
|--------|------|-----------------------------------------------------------------------------|-----------------------------------------|
| UInt16 | 2    | Offset                                                                      | Offset to the string                    
| Byte   | 1    | Received                                                                    | Amount received                         |
| UInt16 | 2    | UNK                                                                         | {0x0001}                                |
| Byte   | 1    | [Input\_Item\_ID](https://github.com/HobbitDur/FF8GameData/wiki#item-list)  | Input: Item id value **0x00**-**0xC6**  |
| Byte   | 1    | Required                                                                    | Amount needed                           |
| Byte   | 1    | [Output\_Item\_ID](https://github.com/HobbitDur/FF8GameData/wiki#item-list) | Output: Item id value **0x00**-**0xC6** |

## m002.bin

### Data

2 abilities

| Ability                                 | \# of Entries | mngrp.bin Location         | Offset | Description                                |
|-----------------------------------------|---------------|----------------------------|--------|--------------------------------------------|
| [[Mid-Mag-RF\|Refinement#mid-mag-rf]]   | 4 entries     | (mngrp.bin loc: 0x220000) | 0x0    | Upgrade Magic from low level to mid level  |
| [[High-Mag-RF\|Refinement#high-mag-rf]] | 6 entries     | (mngrp.bin loc: 0x220020) | 0x20   | Upgrade Magic from mid level to high level |

### Entry

8 bytes

| Type   | Size | Value                                                                          | Description                              |
|--------|------|--------------------------------------------------------------------------------|------------------------------------------|
| UInt16 | 2    | Offset                                                                         | Offset to the string                     
| Byte   | 1    | Received                                                                       | Amount received                          |
| UInt16 | 2    | UNK                                                                            | {0x0001}                                 |
| Byte   | 1    | [Input\_Spell\_ID](https://github.com/HobbitDur/FF8GameData/wiki#magic-items)  | Input: Spell id value **0x01**-**0x38**  |
| Byte   | 1    | Required                                                                       | Amount needed                            |
| Byte   | 1    | [Output\_Spell\_ID](https://github.com/HobbitDur/FF8GameData/wiki#magic-items) | Output: Spell id value **0x01**-**0x38** |

## m003.bin

### Data

1 abilities

| Ability                            | \# of Entries | mngrp.bin Location        | Offset | Description                                       |
|------------------------------------|---------------|---------------------------|--------|---------------------------------------------------|
| [[Med LV Up\|Refinement#med-lv-up]] | 12 Entries    | (mngrp.bin loc: 0x220800) | 0x0    | Level up low level recovery items to higher items |

### Entry

8 bytes

| Type   | Size | Value                                                                       | Description                             |
|--------|------|-----------------------------------------------------------------------------|-----------------------------------------|
| UInt16 | 2    | Offset                                                                      | Offset to the string                    
| Byte   | 1    | Received                                                                    | Amount received                         |
| UInt16 | 2    | UNK                                                                         | {0x0001}                                |
| Byte   | 1    | [Input\_Item\_ID](https://github.com/HobbitDur/FF8GameData/wiki#item-list)  | Input: Item id value **0x00**-**0xC6**  |
| Byte   | 1    | Required                                                                    | Amount needed                           |
| Byte   | 1    | [Output\_Item\_ID](https://github.com/HobbitDur/FF8GameData/wiki#item-list) | Output: Item id value **0x00**-**0xC6** |

## m004.bin

### Data

1 abilities

| Ability                          | \# of Entries | mngrp.bin Location        | Offset | Description   |
|----------------------------------|---------------|---------------------------|--------|---------------|
| [[Card Mod\|Refinement#card-mod]] | 110 Entries   | (mngrp.bin loc: 0x221000) | 0x0    | Card to Items |

### Entry

8 bytes

| Type   | Size | Value                                                               | Description                     |
|--------|------|---------------------------------------------------------------------|---------------------------------|
| UInt16 | 2    | Offset                                                              | Offset to the string            
| Byte   | 1    | Received                                                            | Amount received                 |
| UInt16 | 2    | UNK                                                                 | {0x0001}                        |
| Byte   | 1    | Card\_ID                                                            | Card id value **0x00**-**0x6D** |
| Byte   | 1    | Required                                                            | Amount needed                   |
| Byte   | 1    | [Item\_ID](https://github.com/HobbitDur/FF8GameData/wiki#item-list) | Item id value **0x00**-**0xC6** |

# MSG

Text offsets are in [bin](#BIN) files, and are
classic [FF8 String]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8String)

## Function addresses

| Function | Address | Description |
|---|---|---|
| `Menu_Prog19_RefineMenu_Init` | 0x4D7180 | Refine menu program init; loads the m00x mngrp copies |