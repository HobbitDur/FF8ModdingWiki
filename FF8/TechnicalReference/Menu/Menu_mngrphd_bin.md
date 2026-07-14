---
layout: default
parent: Menu
title: Mngrphd.bin File Format
permalink: /technical-reference/menu/mngrphdbin-file-format/
---

This is the map for [Mngrp.bin](../mngrpbin-file-format/). Locations to data and the size of the section.

The file contains **256 entries** of 8 bytes (2048 bytes total). **118 entries are valid** (they describe the 118 sections of mngrp.bin); the other 138 are invalid placeholders. Two invalid markers exist in the retail file:

* Seek = **0xFFFFFFFF** with Size = 0 (88 entries, interleaved between valid ones)
* Seek = **0x00000000** with Size = 0 (50 entries, at the end of the file, slots 206-255)

Invalid entries need to be kept or the game crashes: the engine addresses this table by **raw entry index** (entry = file start + 8 × index), and those indices are hardcoded in the executable (for example the refine menu loads entries 188-192 and 196-200). Removing a placeholder shifts every following index.

## Entry

| Type   | Size | Value | Description                                                                                                                                                     |
|--------|------|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UInt32 | 4    | Seek  | Location of data. **Bit 0 is a flag** (see below); the actual location is `Seek & ~1`, so for a normal entry the stored value is the location **+ 1**. (**{0xFFFFFFFF}** and **{0x00000000}** values are invalid.) |
| UInt32 | 4    | Size  | Total Size of all data at this location, always a multiple of 0x800. (**{0x00000000}** values are invalid.)                                                     |

## Seek bit 0: compression flag

Bit 0 of the Seek value tells the engine how the section is stored:

* **Bit 0 set** (all 118 valid entries in the retail PC file): the section is stored uncompressed and is copied as-is from mngrp.bin at `Seek - 1`.
* **Bit 0 clear**: the section is LZS-compressed; the engine reads it from `Seek` and decompresses it into the destination buffer. This is a PlayStation leftover — no PC section uses it, but the code path still exists.

This is why tools that simply "subtract 1 from the seek" work on the retail file: since sections are 0x800-aligned, storing location + 1 is the same as setting bit 0 on an aligned offset.

## Engine addresses (FF8 PC 2000, FF8_EN.exe)

| Address  | Name                       | Role                                                             |
|----------|----------------------------|------------------------------------------------------------------|
| 0x4AC0A0 | Menu_FileLoadQueue_Process | Reads an entry by raw index and dispatches raw copy vs LZS path  |
| 0x52D770 | File_LoadRange_LZSDecompress | Loads a file range and LZS-decompresses it (bit 0 clear path)  |
| 0x5305D0 | LZS_DecompressBuffer       | LZS decompressor (4-byte size header, 12-bit window)             |
| 0x1D2BB18 | mngrphd_binBuffer         | The whole file, loaded once by MenuReadFiles                     |
