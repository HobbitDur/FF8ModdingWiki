---
layout: default
title: Field rendering and collision runtime
parent: Field
permalink: /technical-reference/field/rendering-collision/
---

1. TOC
{:toc}

# Field rendering and collision runtime

How the engine turns the field files into the running scene each frame: background tiles, depth, walkmesh movement, triggers and effects. The file formats themselves (.mim/.map/.id/.ca/.inf/.pmd) are documented in the Field File Format section; this page is the runtime view. Addresses for FF8_EN.exe, image base 0x400000.

## Background rendering

* **Texture caching** — the `.mim` is blitted into the emulated 1024×512 PSX VRAM: palettes at (0,232), tile pixels as 16 strips of 832×16 from y=256. The generic psxvram layer converts texture pages to DirectX surfaces on demand.
* **Tile list** — `Field_BG_BuildTileDrawList` re-walks the raw `.map` records (16 bytes/tile) **every frame**, emitting a 16-byte sprite primitive per visible tile (with DR_TPAGE prims on texture-page changes) into double-buffered prim buffers.
* **Scroll and parallax** — per-layer screen position = tile.xy + camera pan × parallax/256 + script scroll; `.inf` byte 15 is the parallax-enable mask and `.inf+22` holds per-layer wrap sizes (layers wrap when scrolled out of bounds). The whole-screen pan is applied as display-environment offsets (`Field_BG_UpdateScreenScroll`, includes shake).
* **State/animation tiles** (doors, lights) — tile byte 14 = state group, byte 15 = state value; a tile draws only when its value matches the group's current state in the 4-byte/group state table ({R,G,B,state}). The RGB part is tweened by controller structs (current/target color + timer) — this is BGANIME/light-flicker. Door triggers flip the states through script entity flags.
* **Depth** — one Z ordering table per frame (0..4095, inside the double-buffered render context): tiles insert at their `.map` Z, character polygons and shadows insert at GTE-projected Z — so per-tile occlusion of characters costs nothing.
* **FMV fields** — `.inf` byte 14 = 1 makes `Field_BG_CaptureVramForMovieMask` snapshot the background and the `.msk` file keeps foreground tiles above the movie.

## Walkmesh and movement

Triangles are 24 bytes (3 × int16 xyz verts) with a 3×int16 adjacency table and a script-lockable per-triangle **blocked bitfield**. Entities (612-byte structs) carry fixed-point position, current triangle, collision radius, speed scale and facing.

* **Movement step** (`Field_Walkmesh_MoveEntityStep`): probes facing ±32 and straight rays with slope-attenuated speed; each ray also runs the entity-vs-entity cylinder test; the entity auto-rotates ±8 toward the free ray — that's the wall slide.
* **Triangle transitions** (`Field_Walkmesh_ResolveMovement`): 2D cross-product edge tests; leaving an edge hops to the adjacency neighbor unless it is −1 or blocked (wall + slide hint). Height always comes from the triangle plane equation — smooth slopes and stairs.
* **Entity collision** (`Field_Collision_EntityVsEntities`): cylinder test on summed radii with height difference < 128; sets the touched flag consumed by TOUCH script events; through/push flags respected.

## Triggers

* **Gateways** (field exits, `.inf`+100, 12×32 B): line P1/P2, destination X/Y, destination walkmesh triangle, destination field id (< 0x48 = world map) and facing. A gateway fires when the player is within touch radius **and** the cross-product sign against the line flips between the old and new position. Spawn placement on the destination field uses the stored triangle (`Field_Walkmesh_PlaceEntitiesOnLoad`).
* **LINE triggers** (script LINE/LINEON): lines live in the script-entity structs; `Field_Collision_UpdateLineTriggerFlags` latches WITHIN/LEAVE/CROSS/TOUCH/TALK/PUSH event flags that the script dispatcher consumes. Talk/push additionally require facing within 64/256 angle units and a button edge while stationary.
* **Door triggers** (`.inf`+484, 12×16 B, modes 0–5): raise open/close request flags on the target script entity (`Field_Collision_FireDoorTrigger`) — sliding doors and background state flips.

## Characters, shadows, effects

The `.ca` camera is parsed per frame; characters are posed (with head-tracking clamped to per-entity max angles) and rendered into the shared ordering table at projected Z. Circle shadows are 8 projected octagon segments with per-vertex radius/darkness. The PMD particle layer runs 16 emitters (254 B each) spawning into 128 particle slots of 32 bytes, camera-transformed as sprites (the `Field_FX_*` function family); save/draw-point pulses are 8 dedicated slots gated by the SetSavePoint state.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `Field_MainLoop_UpdateFrame` | 0x4767B0 | Per-frame field update |
| `Field_BG_BuildTileDrawList` | 0x475480 | Rebuilds the background tile draw list from `.map` |
| `Field_BG_UpdateScreenScroll` | 0x476450 | Applies pan/scroll/shake display offsets |
| `Field_BG_UpdateScreenFade` | 0x47B980 | Screen fade update |
| `Field_BG_CaptureVramForMovieMask` | 0x472A60 | Snapshots background for FMV masking |
| `Field_Chara_UpdateEntitiesMotion` | 0x4789A0 | Updates character entity motion |
| `Field_Chara_SetModelPoseAndHeadLook` | 0x472B30 | Poses models and applies head-tracking |
| `Field_Chara_DrawCircleShadows` | 0x472F20 | Draws octagon circle shadows |
| `Field_FX_UpdateParticleEmitters` | 0x473DE0 | Updates the PMD particle emitters |
| `Field_FX_EmitterStepAndSpawn` | 0x473C50 | Steps and spawns particles for an emitter |
| `Field_FX_InitParticleSystem` | 0x4743D0 | Initializes the particle system |
| `Field_Walkmesh_MoveEntityStep` | 0x479C60 | Movement step and wall-slide probing |
| `Field_Walkmesh_ResolveMovement` | 0x47A3E0 | Triangle-to-triangle transition resolution |
| `Field_Walkmesh_HeightOnTriangle` | 0x47A680 | Height from the walkmesh triangle plane |
| `Field_Walkmesh_PlaceEntitiesOnLoad` | 0x477C90 | Spawns entities on their destination triangle |
| `Field_Collision_EntityVsEntities` | 0x47A720 | Entity-vs-entity cylinder collision test |
| `Field_Collision_UpdateLineTriggerFlags` | 0x4775C0 | Latches LINE trigger event flags |
| `Field_Collision_CheckGatewayCrossing` | 0x477980 | Gateway line-crossing test |
| `Field_Collision_CheckInfDoorTriggers` | 0x47B610 | Door trigger check from `.inf` |
| `Field_Collision_CheckTalkPushButton` | 0x4777F0 | Talk/push button-edge check |
| PSX VRAM buffer | 0x1B46618 | Global variable/data, not a function — emulated 1024×512 PSX VRAM |
| BGANIME state table | 0x1A77238 | Global variable/data, not a function — per-group tile state/color table |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
