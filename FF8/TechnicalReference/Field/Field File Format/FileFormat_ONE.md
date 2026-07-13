---
layout: default
parent: Field File Format
title: Field Character Models Container
permalink: /technical-reference/field/field-file-format/field-character-models-container/
---

By myst6re. Header variants, name field layout, scale location and the headerless format documented from a survey of all 873 PC chara.one files (2026).

# chara.one Archive

Each field contains a chara.one file that contains multiple field models (NPCs), or calls to main character models (Squall, Laguna...). NPC models are stored inline as [MCH](FileFormat_MCH) model data (without the 256-byte header); main characters are stored as a name reference plus the animations they use on this field — their geometry lives in `main_chr.fs` (d0xx.mch).

There are two layouts on PC: the common **headered** layout below, and a rarer **headerless** layout (see the last section).

## Header

| Offset               | Length                           | Description                                   |
|----------------------|----------------------------------|-----------------------------------------------|
| 0x00                 | 4 bytes                          | Number of models (not present in ps version!) |
| 0x04                 | nbModels \* varies bytes         | Model headers                                 |
| 0x04 + nbModels\*var | 256-(0x04 + nbModels\*var) bytes | Padding (the header is always 256 bytes)      |

### Model header

For each model. Beware: several fields are optional and their presence varies **per file**, so a robust parser must detect them (rules given per row).

| Offset        | Length  | Description                                                                                                                     |
|---------------|---------|---------------------------------------------------------------------------------------------------------------------------------|
| 0x00          | 4 bytes | Offset to model textures + data. Warning: in pc version, you must add 4 to this offset!                                         |
| 0x04          | 4 bytes | Size of model data (often includes sector-alignment padding)                                                                    |
| 0x08          | 4 bytes | Size of model data (bis). OPTIONAL: present only when equal to the previous DWORD — check before consuming                      |
| next          | 4 bytes | If this DWORD &gt;&gt; 24 == 0xd0: main character model. Bits 8–23 hold the model scale (scale = value / 16, typically 0x1000 → 256). No TIM list and no model data in this file: the data block holds only the animation section |
| next          | Varies  | NPC only: TIM offset list (relative to the "Offset to model textures + data"), ends with value 0xFFFFFFFF. The high nibble of each DWORD holds flags, not offset bits: the engine reads offsets as `value & 0x0FFFFFFF` and treats any negative DWORD as the terminator. A DWORD with high nibble 0xA replaces the whole list with a single shared-texture reference (see below). See the [MCH page](FileFormat_MCH) for the countdown flag found in multi-texture lists |
| next          | 4 bytes | Model data offset (relative to the "Offset to model textures + data"), also masked `& 0x0FFFFFFF` by the engine; 0 for main character models |
| next          | 8 bytes | OPTIONAL: model name as 4 ASCII characters (e.g. `d000`, `p065`) followed by 4 unknown bytes (often `60 70 80 00`). Present only when the 4 bytes are printable — some files omit the whole field |
| next          | 4 bytes | Shared-texture entries only: the referenced entry index again (same value as bits 20–27 of the 0xA DWORD)                       |
| next          | 4 bytes | OPTIONAL: end marker 0xEEEEEEEE. Some files omit it                                                                             |

### Shared-texture entries

Some NPC variants carry no texture of their own and reuse the texture of another model in the same file (e.g. `gfrich1a`: `o182`–`o186` reuse `o181`'s TIM). Their TIM offset list is a single DWORD of the form `0xA0000000 | (entry_index << 20) | low_bits`:

- Bits 28–31: 0xA marker. The engine checks `(value & 0xF0000000) == 0xA0000000` and, instead of uploading a TIM, copies the VRAM texture/CLUT ids already registered for the referenced model.
- Bits 20–27: index of the referenced entry in this file.
- Bits 0–19: point inside the referenced entry's data block (consistently its last 0x800-byte sector in the vanilla files); not read by the PC engine.

The data block of such an entry contains only model data (no TIM), and its header carries one extra DWORD after the name field repeating the referenced entry index. 24 of the 862 headered PC files contain such entries (60 models, all `oXXX` object variants): `bgmd2_6`, `bgpaty_1`, `bgsido_4`, `bgsido_7`, `bgsido_9`, `efenter2`, `feyard1`, `fhwise12`, `fhwise13`, `gfrich1`, `gfrich1a`, `ggkodo2`, `gmout1`, `gmpark1`, `gmpark2`, `gmtika2`, `gnroom4`, `gpbig1`, `gpbigin3`, `sspack1`, `tihtl1`, `timania1`, `tmelder1`, `tvglen5`.

## Data

For NPCs: TIM textures at the listed offsets, then model data using the same structure as an [MCH model](FileFormat_MCH) (without header). The NPC's field animations are inside the model data, at its "offset of animation data", in the packed 4-byte pose format described on the [MCH page](FileFormat_MCH).

For main characters: the data block is just the animation section (packed format, starting with the uint16 animation count). The game loads the geometry from `main_chr.fs` using the model name.

In the PlayStation version, each model textures + data is LZS compressed.

## Headerless variant

A small number of PC field files (11 of 873; e.g. `bccent12`, `bccent15`, `bg2f_1a`, `doani2_1`) keep a PS-style layout with no model count and no model headers:

| Offset | Length | Description                                  |
|--------|--------|----------------------------------------------|
| 0x00   | 4 bytes| EOF (equals the file size — use this to detect the variant) |
| 0x04   | ...    | Raw TIM and model-data chunks back to back (uncompressed on PC) |

Chunks must be identified by scanning: a TIM starts with `10 00 00 00` followed by a flag DWORD in {0x02, 0x03, 0x08, 0x09}; anything else is model data belonging to the TIMs that precede it.

## Runtime notes

The 64-byte bone records of the model data are used directly by the engine as its runtime skeleton records, and the engine adds a "pre-root" record with a constant RotY(+90°) above every model — see the [MCH page](FileFormat_MCH) runtime section for the full skeleton/animation pipeline (FF8_EN.exe function addresses included).
