---
layout: default
parent: Menu
title: TknmnesX.bin File Format
permalink: /technical-reference/menu/tknmnesxbin-file-format/
---
These files have a good deal of the Menu text.

3 files are concerned:
* tknmnes1.bin
* tknmnes2.bin
* tknmnes3.bin

Note that those files are actually not use, but instead the one contains in the archive [Mngrp.bin](../mngrpbin-file-format/)

The data consist of a header that contains the __paddings__, corresponding to the offset to string section. Each string section contains a list of offset, followed by the strings.

# Header

Padding values **0x0000** must be ignored when reading but must be kept in the same place when writing.

| Type   | Size          | Value     | Description                                                                                                               |
|--------|---------------|-----------|---------------------------------------------------------------------------------------------------------------------------|
| UInt16 | 2             | Pad_Count | The number of padding. Always **16**.<br/>The real number of padding is the value read + 1 (so 17 in unmodified file).                                                                                    |
| UInt16 | 2 * Pad_count | Paddings  | The padding value leads to the start of string section offsets.<br/> **0x0000** must be ignored.  |

# String section
Each string section correspond to a [Mngrp string section](../mngrp-string-section/)

**\[Start of string location\]** = **\[Start of file\]** + **\[Padding value\]** + **\[String offset value\]**
