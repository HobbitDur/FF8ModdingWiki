---
layout: default
title: WorldMap terrain rendering and streaming
parent: WorldMap
permalink: /technical-reference/worldmap/terrain-streaming/
---

1. TOC
{:toc}

# WorldMap terrain rendering and streaming

How the engine streams `wmx.obj` around the player and turns it into triangles each frame. Complements the [wmx format]({{ site.baseurl }}/technical-reference/worldmap/worldmap-wmx/) and [texl]({{ site.baseurl }}/technical-reference/worldmap/worldmap-texl/) pages with the runtime view. Addresses for FF8_EN.exe, image base 0x400000.

## Map layout recap

The world is a 32×24 grid of **segments** (8192 units each); a segment holds 4×4 **squares** (2048 units). Segment id = col + 32×row, toroidally wrapped. In `wmx.obj` a segment is a fixed **0x9000-byte** record at offset `36864 × fileSegIdx` — no compression.

## Segment streaming (`Wmx_UpdateSegmentStreaming`, 0x5531F0)

* The **wanted set** is rebuilt every frame: all segments within ±12287 units (up to a 4×4 area) of the look-ahead streaming center — a point 6144 units ahead of the camera (`World_ComputeCameraLookAheadPoint`), not the player itself.
* Four linked lists of 12-byte nodes track state: *pending* → *loading* → *loaded*, plus a free list. Only **one** segment read is in flight at a time (async `Archive_IO_LoadFile` of 0x9000 bytes straight into a cache slot).
* The cache has **16 slots**; a new segment takes the first free slot, or steals the slot of a loaded segment no longer in the wanted set.
* **Alternate world states** — story flags in `wm_worldStateFlags` (Fisherman's Horizon bridge, the Lunar Cry crater, the shield around it, …) remap `fileSegIdx` through tables at 0xC763D2/0xC763EE (`Wmx_ApplyAlternateSegmentRemap`) before the read, which is how replacement segments stored later in wmx.obj appear transparently.
* The same pump streams **texl.obj detail pages**: each segment header names its detail page (byte 0, 0xFF = none); two pages stay resident (0x12800 bytes each, uploaded as 128×256 texture + CLUTs). Pages 2/3 remap +12 under state flag bit 0 (post-FH-battle Horizon).

## Runtime structures

**Segment header**: `+0` texl detail page id, `+4` int[16] block byte-offsets (one per square, index = x%4 + 4·(y%4), low 2 bits masked).

**Block (one square)**: `+0` u8 triangle count, `+1` u8 vertex count, `+2` u16 normal count, then 16-byte triangles, then 8-byte vertices (SVECTOR), then 8-byte normals.

**Triangle (16 bytes)**:

| Offset | Meaning |
|--------|---------|
| 0–2 | vertex indexes |
| 3–5 | normal indexes |
| 6–11 | three U,V pairs |
| 12 | texture info: default = high nibble+224 → tpage, low bits → CLUT (UVs halved); with flag bit 5 = index into the animated-texture table; with bit 6 = texl detail page |
| 13 | terrain type (walkmesh material; also drives footstep/particle effects and script conditions) |
| 14 | flags: bits 0–1 shade level, bit 4 semi-transparent, bit 5 animated texture, bit 6 texl detail |
| 15 | vehicle walkability mask: bit 7 foot/chocobo, bit 6 buggy, bit 5 Ragnarok, bit 4 vehicle 49 |

## Per-frame rendering

`World_UpdateAndDrawTerrain_Fog` (0x53BB90) or `_NoFog` (0x53C750, selected once per frame by the `WORLDMAP_WITHOUT_FOG` registry bit) orchestrates:

1. **Ground probes** — 2 sets × 8 rows of 5 probes (44-byte records: world pos, segment-local pos, resolved triangle ptr, ground height, terrain type, state) are placed around the player/vehicles (`World_SetupGroundProbeRow`) and resolved against square blocks (`World_ResolveGroundProbes`, with an MRU triangle cache) using `World_PointInTriangleGetHeight` — an XZ point-in-triangle test with plane-interpolated height. This is the ground query every vehicle altitude/walkability check uses (`World_IsTriangleWalkable` tests the vehicle mask at tri+15).
2. **Visible square list** — frustum-culled (`World_CullVisibleSquareList`) around the camera.
3. **Near blocks** — full triangle emission per square (`World_DrawNearBlock_*`, with fog-overlay and Ragnarok-flight variants): vertices are camera-relativized and sunk by the horizon-curvature function (`World_PretransformBlockVertices`, curvature starts at `wm_curvatureStartDist`), projected (`World_ProjectTerrainVertices`), then emitted with per-triangle texture/CLUT selection and shade level.
4. **Far blocks** — `World_DrawFarTerrainBlock` renders distant squares with the same curvature sink and texl detail LOD swap.
5. **Texture animation** — beach/waterfall strips are advanced each frame by inline code in the world main loop (~0x540A8E) that updates the animated CLUT/tpage table and re-uploads 256×1 strips (`wmsets41_parse`).

## Address table

| Function | Address | | Function | Address |
|----------|---------|-|----------|---------|
| `Wmx_UpdateSegmentStreaming` | 0x5531F0 | | `World_ResolveGroundProbes` | 0x53E2A0 |
| `Wmx_ApplyAlternateSegmentRemap` | 0x553980 | | `World_PointInTriangleGetHeight` | 0x402620 |
| `Wmx_GetSquareBlockPtr` | 0x553E00 | | `World_IsTriangleWalkable` | 0x53E6B0 |
| `Wmx_FindSegmentNode` | 0x553960 | | `World_PretransformBlockVertices` | 0x4022D0 |
| `World_UpdateAndDrawTerrain_Fog` | 0x53BB90 | | `World_ProjectTerrainVertices` | 0x4023D0 |
| `World_UpdateAndDrawTerrain_NoFog` | 0x53C750 | | `World_SetupGroundProbeRow` | 0x53D8A0 |
| `World_DrawNearBlock_Fog` / `_NoFog` | 0x552380 / 0x553FD0 | | `World_CullVisibleSquareList` | 0x53D3C0 |
| `World_DrawNearBlock_RagnarokFlight_Fog` / `_NoFog` | 0x5519B0 / 0x5543A0 | | `wmx_segmentCache` (16 slots) | 0xC75D04 |
| `World_DrawFarTerrainBlock` | 0x5513A0 | | `wm_worldStateFlags` | 0x2036BB6 |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
