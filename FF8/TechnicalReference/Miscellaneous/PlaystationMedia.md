---
layout: default
parent: Miscellaneous
title: Playstation Media
permalink: /technical-reference/miscellaneous/playstation-media/
---

By myst6re

# FF8DISCX.IMG File Format

Almost all of the game files are hidden in the FF8DISCX.IMG (with X=disc number) file.

## Root Files

In the case of a Japanese iso, the file begins directly with a list of file location and size, with the following format:

| Offset | Size | Data                                                               |
|--------|------|--------------------------------------------------------------------|
| 0      | 4    | Location of file in sectors (relative to the start of the **iso**) |
| 4      | 4    | Size of file in bytes                                              |

In the case of a PAL iso, there are 5 unknown sectors (a sector = 2048 bytes in data, 2352 bytes in disk) before this list of files.

**Notes:**

-   I do not have the American iso, please fix this article if you can.
-   We do not know how many files there are in the list, neither file names!
-   Each file in FF8DISCX.IMG are relative to the start of the **iso**!

| ID           | Filename (from PC version)                             | Notes                             |
|--------------|--------------------------------------------------------|-----------------------------------|
| 0            | ? + packcode.bin                                       | Contains a font file (tim format) |
| 1            | images.lzs                                             | Main images (CD + credits)        |
| 2            | [field.bin](#field-files)                              | LZSed                             |
| 3            | wm2field.tbl                                           | size= 72\*24 bytes                |
| 4            | ? + mmagic.bin + mitem.bin + areames.dc1 + ?           |                                   |
| 5            | ? + mmagic.bin + mitem.bin + areames.dc1 + ?           |                                   |
| 6            | Menu (pty)                                             |                                   |
| 7            | ? + pet\_exp.bin + ?                                   |                                   |
| 8            | Menu (abilities)                                       |                                   |
| 9            | ? + mwepon.bin + mwepon.msg + shop.bin + price.bin + ? |                                   |
| 10           | Menu (ext)                                             |                                   |
| 11           | ? + mmag.bin + mthomas.bin                             |                                   |
| 12           | ? + magsort.bin                                        |                                   |
| 13           | Menu (GF)                                              |                                   |
| 14           | Menu (jnc2)                                            |                                   |
| 15           | ? + mmag2.bin + cyocobo.bin                            |                                   |
| 16           | ? + cardanm.sp2                                        |                                   |
| 17           | ? + mtmag.bin                                          |                                   |
| 18           | Menu (mag)                                             |                                   |
| 19           | Menu (ips)                                             |                                   |
| 20           | Menu (est)                                             |                                   |
| 21           | mngrp.bin                                              |                                   |
| 22           | init.out                                               |                                   |
| 23           | Triple Triad (in ff8.exe in PC version)                | Some Triple Triad tims (LZSed)    |
| 24           | battle_font.bin (not present in PC version)            |                                   |
| 25           | battle.bin (not present in PC version)                 |                                   |
| 26           | [world.bin](#world-files)                              | LZSed                             |
| 27 -&gt; 28  | AKAO files (music/sound)                               |                                   |
| 29           |                                                        |                                   |
| 30 -&gt; 127 | AKAO files (music)                                     |                                   |
| 128          | kernel.bin                                             |                                   |
| 129          | sysfnt.tdw                                             |                                   |
| 130          | icon.tim                                               |                                   |
| 131          | namedic.tim                                            |                                   |
| 132          | AKAO file (music/sound)                                |                                   |
  

## Field Files

In the list of root files, the third file is in fact the "FIELD.BIN". This file is LZS compressed, and contains some informations, like the list of field files position and size.

Find the file list is approximate, I am trying to find some bytes: "\\x04\\x00\\x05\\x24\\x18\\x00\\xbf\\x8f\\x14\\x00\\xb1\\x8f\\x10\\x00\\xb0\\x8f\\x20\\x00\\xbd\\x27\\x08\\x00\\xe0\\x03\\x00\\x00\\x00\\x00" (size=28), normally, there is the list right after this sequence of bytes, and before the "\\x00\\x00\\x01\\x00\\x02\\x00\\x03\\x00" (size=8) sequence.

Order of files (sorted by id):

-   D000.[MCH](../Field/Field%20File%20Format/FileFormat_MCH) -&gt; D075.MCH files \[id=0 -&gt; id=76\]
-   Field files (MIM, DAT and LZK) \[id=77 -&gt; id=last\]

There are three LZSed files for each field: EXAMPLE.MIM, EXAMPLE.DAT and EXAMPLE.LZK (Extension names \*.MIM, \*.DAT and \*.LZK found in PC version, field.fs &gt; mapdata.fs &gt; map1.bak). If you want to convert Playstation fields to PC fields format, this is a concatenation of some PC files.

### First file (\*.MIM)

| Offset               | Size     | Data                                                         |
|----------------------|----------|--------------------------------------------------------------|
| 0                    | 4        | Location of section 3 in PSX RAM                             |
| 4                    | 4        | Location of section 4 in PSX RAM                             |
| 8                    | 4        | Unknown data \[PVP\] (was a link, target page no longer exists)        |
| 12                   | 438272   | [Background data \[MIM](../Field/Field%20File%20Format/FileFormat_MIM)\]     |
| 438284 (section 3)   | *Varies* | [Font data \[TDW](../../field/field-file-format/extra-font/)\]           |
| *Varies* (section 4) | *Varies* | [Particle Image Data \[PMP](../Field/Field%20File%20Format/FileFormat_PMP)\] |

### Second file (\*.DAT)

| Offset | Size     | Data                                   | Section Data                                                   |
|--------|----------|----------------------------------------|----------------------------------------------------------------|
| 0      | 4        | Location of section 1 in PSX RAM       | [Triggers & gateways \[INF](../Field/Field%20File%20Format/FileFormat_INF)\]   |
| 4      | 4        | Location of section 2 in PSX RAM       | [Camera \[CA](../Field/Field%20File%20Format/FileFormat_CA)\]                  |
| 8      | 4        | Location of section 3 in PSX RAM       | Walkmesh \[ID\]          |
| 12     | 4        | Location of section 4 in PSX RAM       | [Background infos \[MAP](../Field/Field%20File%20Format/FileFormat_MAP)\]      |
| 16     | 4        | Location of section 5 in PSX RAM       | [Movie cam \[MSK](../Field/Field%20File%20Format/FileFormat_MSK)\]             |
| 20     | 4        | Location of section 6 in PSX RAM       | [Battle rate \[RAT](../Field/Field%20File%20Format/FileFormat_RAT_MRT)\]       |
| 24     | 4        | Location of section 7 in PSX RAM       | [Battle formations \[MRT](../Field/Field%20File%20Format/FileFormat_RAT_MRT)\] |
| 28     | 4        | Location of section 8 in PSX RAM       | Sounds/AKAOs                                                   |
| 32     | 4        | Location of section 9 in PSX RAM       | [Texts \[MSD](../Field/Field%20File%20Format/FileFormat_MSD)\]                 |
| 36     | 4        | Location of section 10 in PSX RAM      | Particle Infos \[PMD\] (was a link, target page no longer exists)        |
| 40     | 4        | Location of section 11 in PSX RAM      | [Scripts \[JSM](../Field/Field%20File%20Format/FileFormat_JSM)\]               |
| 44     | 4        | Location of the end of file in PSX RAM |                                                                |
| 48     | *varies* | Triggers and gateways                  |                                                                |
| ...    | ...      | ...                                    | ...                                                            |

### Third file (\*.LZK)

Almost like the [chara.one](../Field/Field%20File%20Format/FileFormat_ONE) file. The main difference is that the models data are compressed.


## World Files

Like the field.bin, inside the world.bin (not sure exactly where) you have a series of sectors that point to subfiles.


| ID           | Filename (from PC version)                             | Notes                             |
|--------------|--------------------------------------------------------|-----------------------------------|
| 0            | wmx.obj                                                |                                   |
| 1            | wmy.obj                                                |                                   |
| 2            | texl.obj                                               |                                   |
| 3            | rail.obj                                               |                                   |
| 4            | wmsetXX.obj                                            |                                   |
| 5            | chara.one                                              | LZSed                             |
| 6            | music0.obj                                             |                                   |
| 7            | music1.obj                                             |                                   |
| 8            | music2.obj                                             |                                   |
| 9            | music3.obj                                             |                                   |
| 10           | music4.obj                                             |                                   |
| 11           | music5.obj                                             |                                   |
