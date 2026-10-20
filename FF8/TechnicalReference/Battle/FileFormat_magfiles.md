---
layout: default
parent: Battle
title: Mag File Format
author: MaKiPL, HobbitDur
permalink: /technical-reference/battle/mag-file-format/
---

# MAG file family

MAG names identify effect resources, not one binary format. Inspect the contents before choosing a
parser: even a `.00` file can be a TIM texture or a four-byte reference rather than a cinematic.
For conventional `MAGnnn_B.00` cinematics the effect ID is `nnn + 1`; shared texture names do not
necessarily identify a single effect.

The English 2013 Steam executable and the extracted PC `magic/` and `battle/` archives were audited
in October 2026. The 790 MAG/MA8 files in that corpus classify as follows:

| Content | Files | Identification / interpretation |
|---|---:|---|
| PlayStation TIM | 387 | `u32 0x10`, validated TIM blocks; suffix can be `.tim`, `.dat`, `.00`, `.1t0`, etc. |
| Packed MAG | 180 | Validated 0x30-byte section directory and initial resource tables |
| Indexed containers | 61 | Validated count/offset/end directories; includes model/animation/resource parts |
| SCOT sound | 24 | `SCOT` at byte 4, preceded by a four-byte value |
| AKAO audio | 1 | `AKAO` at byte 0 |
| Four-byte references | 32 | Exactly one `u32`; meaning depends on the loader |
| Raw / undecoded | 105 | No validated directory/signature; includes raw streamed pages and effect-specific data |

These are structural classifications, not a claim that every payload has been semantically decoded.
The [machine-readable census](https://github.com/HobbitDur/FF8UltimateEditor/blob/master/docs/mag-file-census.json)
records names, hashes, section counts, script results and camera locations without distributing assets.
The [Laguna editor guide](https://github.com/HobbitDur/FF8UltimateEditor/blob/master/docs/laguna-mag-editor.md)
describes editing and reproduction commands.

1. TOC
{:toc}

## Packed MAG header

Little-endian; header fields are `u32` offsets from the file start. Zero means absent for optional
sections. Empty initial tables can share their end offset with the next table or the root script.

| Header offset | Meaning |
|---|---|
| `0x00` | Reserved/unknown; zero in the audited packed files |
| `0x04` | Root cinematic program, present in 58 audited files |
| `0x08` | CLUT table start; also the texture table end |
| `0x0C` | Object directory: `u32 count`, then `u32 offset[count]` relative to this directory |
| `0x10` | Sound-effect table/data |
| `0x14` | Texture table start (`0x30` in the audited packed files) |
| `0x18` | Music-stream table start; also the CLUT table end |
| `0x1C` | End of initial tables; in GF `.01` parts, the start of runtime workspace |
| `0x20` | Embedded stage camera track, when used; nonzero in 46 audited files |
| `0x24` | Voice-bank data, when present |
| `0x28`, `0x2C` | Reserved/unknown; zero in the audited packed files |

A leading zero alone is not sufficient to identify a packed file: raw VRAM pages can also start
with many zeros. Validate the header, monotonic initial table boundaries, counts and resource targets.

### Resource directories and offset bases

Texture entries occupy `[header[0x14], header[0x08])`; CLUT entries occupy
`[header[0x08], header[0x18])`. Entries are four bytes. A nonzero entry identifies data at
`table_start + (entry & 0x00FFFFFF)`; do not treat the upper byte as part of the byte offset.
Object entries use their full relative offset from the **object directory start**. Header entries
are relative to the **file start**. These bases are different.

The cinematic GF resource tables use global resource IDs shared by all loaded parts. A zero entry
can mean that resource ID is held in another file. The per-effect executable descriptor supplies
file slots and texture/CLUT VRAM rectangles; packed texture payload bytes alone do not establish
image dimensions or pixel depth.

Physical spans can be mapped using validated section starts and referenced resource starts. A span
ends at the next known boundary and may include alignment/padding. Preserve unreferenced and unknown
bytes; the map is not a license to discard them or to infer a resource's exact semantic length.

### Script and object resources

The root program uses the cinematic VM: little-endian 16-bit words, low nine bits for the opcode,
remaining bits for opcode-specific modifiers. Operands and inline data determine instruction length.
The script region ends at the next section, which may be an embedded camera **before** the sound table.
See [Cinematic script and mag files](GFCinematicScript.md) for instructions, control flow and resources.

Objects are polymorphic: the using opcode decides whether an object is a mesh, model, sprite list
or another structure. Recognized layouts include:

- **Mesh:** 0x30-byte header, primitive list at `+0x08`, vertices at `+0x14`/count `+0x18`,
  normals at `+0x1C`/count `+0x20`. Vertices are eight-byte `{s16 x,y,z,pad}` records.
  Primitive groups are `{u16 type,u16 count}` followed by type-specific records; count `0xFFFF`
  terminates the list. Primitive vertex references are byte offsets into the vertex array.
- **Embedded battle model:** seven `u32` values beginning with model size and relative skeleton,
  geometry and animation offsets. The first section starts at `0x1C`; the last directory word is
  `size - 4`. The other variant fields must be preserved rather than assumed zero. Skeleton,
  geometry and animation use the corresponding battle-model section formats.
- **Sprite frame list:** eight-byte entries `{s32 relativeFrame,s16 duration,s8 control,pad}`;
  control 0 continues, 1 ends, 2 loops. Frame references are relative to the object directory.

Detailed primitive layouts are retained in [the object reference](GFCinematicScript.md#objects).
There is no general twelve-object limit: the audited corpus contains 712 packed object entries,
including containers with more than twelve objects.

## Embedded camera tracks

The cinematic opcode word `0x1039` (opcode `0x39`, sub-operation 1) invokes `StageCameraAnim`:

```c
Battle_PlayCameraAnimation(file_base + read_u32(file_base + 0x20));
```

This is the same track format used by static exe effect cameras:

| Track-relative offset | Type | Meaning |
|---|---|---|
| `+0x00` | `u16` | Pointer count, 2 |
| `+0x02` | `u16` | Camera VM script offset, normally 8 |
| `+0x04` | `u16` | Keyframe collection offset |
| `+0x06` | `u16` | Total track byte size |
| `+script` | bytes | Camera VM bytecode, **not** cinematic VM words |
| `+keyframes` | bytes | Camera sets/animation slots/blocks/keyframes |

All 46 camera tracks in the audit parse and rebuild byte for byte, totaling 1,120 keyframe entries.

### Disease Breath, effect 231

The resource loader at EN `0xA66470` opens `MAG230_B.00` and `MAG230_B.01`. The `.00` root is
`0x58`; at file offset `0x5A`, words `1039 0000` start the embedded camera. Header `+0x20`
contains `0x870`. The native call at `0xA6C240` passes this file-derived address to the battle
camera player (`0x5099A0`).

The track spans `[0x870,0x930)`: header words `0002 0008 0018 00C0`, 192 bytes total, a
15-byte camera script plus one alignment byte, then the keyframe collection. Set 0/slot 0 has
three blocks and five keyframe entries. This is a file camera; absence from the static exe-track
list does not mean absence of camera motion.

## TIM texture files

Standard TIM data starts with magic `0x10` and flags. Flags select 4-, 8-, 16- or 24-bit pixel
encoding and whether a CLUT block is present. Each CLUT/image block has a `u32` block byte size,
VRAM X/Y and width/height fields (`u16` each), followed by its data. Width is in 16-bit VRAM words,
so it is not always the displayed pixel width. Validate block lengths and dimensions.

Do not identify TIM solely by the exact flags value `0x09`: the corpus includes other valid flag
values. A filename or payload byte count does not determine dimensions. Packed raw texture pages
are not standalone TIMs and need their executable descriptor/upload context.

## Indexed containers, audio and raw parts

Three directory layouts are structurally recognized, each beginning with `u32 count`:

1. `offset[count]`, then an end offset.
2. An end offset, then `offset[count]`.
3. `offset[count]` with the file length as the implicit end (verified in `mag064_h.02` and `.03`).

Offsets are file-relative in these validated layouts. The first payload starts after the directory;
entries may alias or denote empty parts, and bytes may remain after the declared end. Directory
recognition does not establish the semantics of every part. Some model/animation banks use these
layouts; others remain undecoded.

SCOT/AKAO data and four-byte references require their own runtime interpretation. Raw streamed parts
can be VRAM pages, particle data, animation data or other effect-specific bytes. **Non-packed** does
not mean **raw texture**. Preserve undecoded data and report its status.

## Editing and validation

Laguna opens all 790 audited files and provides section tabs, named fields where decoded, embedded
camera script/keyframe editing, TIM previews, byte editing and section export/replacement. Recognized
embedded model headers/skeletons/geometry/animations are split into separate tabs. Unknown data remains
editable as bytes. Editing keeps the existing size; relocating larger sections is not implemented.

The audit finds 58 script-bearing packed files. Per-effect runtime opcode profiles and fourteen
additional native-verified opcode encodings let their reachable programs decode without errors.
This is not a full simulation of every effect: playback remains verified for the seven documented
GF summons, while other effects' script/resource data can be edited.

Validation covers complete non-overlapping byte-span coverage, all-file unchanged save round trips,
fixed-size edits/undo and preservation of bytes outside an edited camera. Original game assets are
required to reproduce the full corpus tests and are not included in the repository.

For conventional procedural spell dispatch and resources, see [Magic Spell Effect Runtime](MagicSpellEffectRuntime.md)
and [Magic Effect Anatomy](MagicEffectAnatomy.md). For the seven GF examples and streamed file slots,
see [Cinematic script and mag files](GFCinematicScript.md).
