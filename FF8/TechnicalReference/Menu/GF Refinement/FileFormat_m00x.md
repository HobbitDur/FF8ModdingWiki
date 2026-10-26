---
layout: default
parent: GF Refinement
title: Refine abilities
permalink: /technical-reference/menu/gf-refinement/refine-abilities/
author: HobbitDur
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
A m00x.bin file is one flat list of entries: which entries each refine ability offers is not in the file
but in [kernel.bin's menu abilities]({{site.baseurl}}/FF8/TechnicalReference/Main/Kernel/18_Menu-abilities)
(see [Recipe slices and limits](#recipe-slices-and-limits)). The tables below are the vanilla kernel.bin's slices.

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
| UInt16 | 2    | Received | Amount received (the refine and its menu window read 2 bytes; the result is capped at 100) |
| Byte   | 1    | Level | [Required GF level](#required-gf-level): 1, or 100 for two m001 refines |
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
| UInt16 | 2    | Received | Amount received (the refine and its menu window read 2 bytes; the result is capped at 100) |
| Byte   | 1    | Level | [Required GF level](#required-gf-level): 1, or 100 for two m001 refines |
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
| UInt16 | 2    | Received | Amount received (the refine and its menu window read 2 bytes; the result is capped at 100) |
| Byte   | 1    | Level | [Required GF level](#required-gf-level): 1, or 100 for two m001 refines |
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
| UInt16 | 2    | Received | Amount received (the refine and its menu window read 2 bytes; the result is capped at 100) |
| Byte   | 1    | Level | [Required GF level](#required-gf-level): 1, or 100 for two m001 refines |
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
| UInt16 | 2    | Received | Amount received (the refine and its menu window read 2 bytes; the result is capped at 100) |
| Byte   | 1    | Level | [Required GF level](#required-gf-level): 1, or 100 for two m001 refines |
| Byte   | 1    | Card\_ID                                                            | Card id value **0x00**-**0x6D** |
| Byte   | 1    | Required                                                            | Amount needed                   |
| Byte   | 1    | [Item\_ID](https://github.com/HobbitDur/FF8GameData/wiki#item-list) | Item id value **0x00**-**0xC6** |

# Required GF level

Entry byte 0x04 is the GF level a refine needs. When the refine menu opens, `Menu_Prog19_RefineMenu_Init` looks through every GF that exists and has learned the selected refine ability, and keeps the highest level among them. A refine is offered only when that level is at least the entry's level byte; otherwise it is shown as not available, like an entry without enough input items.

Every vanilla entry has level 1 except two in m001.bin:

| Ability       | Entry (file index) | Refine                          | Level |
|---------------|--------------------|---------------------------------|-------|
| Tool-RF       | 141                | 100 Curse Spike -> 1 Dark Matter | 100   |
| Forbid Med-RF | 56                 | 10 Shaman Stone -> 1 Hero-trial  | 100   |

The PC executable still computes the highest GF level but discards it: it stores a fixed 100 as the refine level, so every refine is available at any GF level and the level byte has no effect. Storing the computed level instead restores the check (an 18-byte in-place patch at the store; FF8 Gameplay Customizer's Archeology > Refine GF level option does it). The debug flag read by the battle hidden-debug code still forces level 100.

# Recipe slices and limits

A refine ability takes its recipes from a slice of one table. Its menu ability entry in kernel.bin holds the
table (byte 0x05, 0-4 = m000-m004) and the first and last entry of the slice (bytes 0x06 and 0x07, inclusive).
`Menu_Prog19_RefineMenu_Init` sets the entry count to `last - first + 1` and points the list at
`Menu_RefineEntryBuffer + 8 * first`. Abilities of the same table do not need to follow the file order:
vanilla Tool-RF (4th refine ability of m001 in kernel.bin) offers entries 111-142, the end of m001.bin.

The refine screen lists the player's items (Card Mod: the owned cards), not the recipes. For the highlighted
item, the menu takes the first entry of the slice whose input is that item, so each input has at most one recipe per
ability: a later entry with the same input never shows.

Adding a recipe means inserting an entry and its text, then moving the first/last bytes of every ability of that
table whose slice starts or ends after it. Nothing else in the executable depends on the counts:

| Limit                     | Value        | Reason                                                                      |
|---------------------------|--------------|-----------------------------------------------------------------------------|
| Entries per table         | 256          | `Menu_RefineEntryBuffer` is 0x800 bytes, `Menu_RefineOwnedCardList` follows |
| Entries per ability       | 255          | The entry count of the refine task is one byte                              |
| First / last entry        | 0-255        | One byte each in kernel.bin                                                 |
| Text per table (m00x.msg) | 0x5000 bytes | `Menu_RefineTextBuffer` runs up to `Menu_RefineEntryBuffer`                 |

In mngrp.bin each section is padded with zeros to a multiple of 2048 bytes (the size in mngrphd.bin includes the
padding), so a m00x.bin section ends at its last entry that is not all zeros.

# MSG

Text offsets are in [bin](#BIN) files, and are
classic [FF8 String]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8String)

## Function addresses

| Function                      | Address   | Description                                                                 |
|-------------------------------|-----------|-----------------------------------------------------------------------------|
| `Menu_Prog19_RefineMenu_Init` | 0x4D7180  | Refine menu program init; loads the m00x mngrp copies                       |
| Highest GF level loop         | 0x4D7210  | Highest level among GFs that learned the refine ability, kept at [esp+10h] |
| Refine level store            | 0x4D726A  | Stores the refine level (task+0x47); the PC exe writes a constant 100 here |
| Refine menu update            | 0x4D7410  | Compares the refine level `>=` entry byte 0x04 for each entry               |
| `Menu_RefineTextBuffer`       | 0x1D85864 | m00x.msg of the open refine table (0x5000 bytes)                            |
| `Menu_RefineEntryBuffer`      | 0x1D8A864 | m00x.bin of the open refine table (0x800 bytes)                             |
| `Menu_RefineOwnedCardList`    | 0x1D8B064 | Card Mod's list of owned cards, right after the entry buffer                |