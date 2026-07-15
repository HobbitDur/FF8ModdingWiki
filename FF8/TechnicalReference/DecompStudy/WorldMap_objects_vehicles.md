---
layout: default
title: WorldMap objects and vehicles
parent: WorldMap
permalink: /technical-reference/worldmap/objects-vehicles/
---

1. TOC
{:toc}

# WorldMap objects and vehicles

Runtime companion to the [module runtime]({{ site.baseurl }}/technical-reference/worldmap/module-runtime/) and [script VM]({{ site.baseurl }}/technical-reference/worldmap/script-vm/) pages: how the world map manages its object instances (vehicles, trains, the player, special models) each frame. Addresses for FF8_EN.exe, image base 0x400000.

## Object instance table

Every visible world object is an entry in `world_object_instances` (up to 64 entries of 40 bytes, count in `world_object_count`). The table is rebuilt on world load by `World_BuildObjectInstanceList` from the wmset spawn script (opcodes FF13/FF14) plus savemap state.

| Offset | Type | Meaning |
|--------|------|---------|
| 0x00 | s32 | world X |
| 0x04 | s32 | altitude |
| 0x08 | s32 | **negated** world Y (engine convention) |
| 0x0C | s32 | spawn info (low word = initial yaw source) |
| 0x10 | u8 | model id (wmset object model) |
| 0x11 | u8 | anim mode 0–4 (1 = spin Z, 2 = set Y, 3 = spin Y, 4 = fixed pitch + spin Z — propellers, windmills) |
| 0x12 | s8 | model slot for animated models (< 64); −1 = static wmset model (id ≥ 64) |
| 0x13 | s8 | in-range flag (on loaded map area; required for touch/board and script FF17) |
| 0x14 | s16×3 | rotation pitch / yaw / roll |
| 0x1C | s16×3 | camera-relative render position |
| 0x24 | u8 | visible (on-screen this frame; tested by script FF17) |

A secondary 4-entry table (`world_extra_object_instances`) uses the same layout. Reserved slot indexes (0xC76640–0xC7665C) track the player, two ships, Balamb Garden, the rental car, both Ragnarok instances, and a **Jumbo Cactuar object that only spawns while GF Cactuar is not owned**.

Per frame, `World_UpdateAndPlaceEntityModels` recomputes in-range flags and relative positions (with map wrap-around), applies anim-mode rotations, projects objects on the walkmesh, and draws (`World_DrawObjectShadow` adds the 2-quad projected shadow). `World_FindTouchedObject` scans for collision and facing (`world_touched_object_idx` / `world_facing_object_idx` — consumed by script conditions FF1A–FF1D).

## Vehicles

Verified vehicle id mapping (see the module-runtime page table): 0–9/128 on foot, 16–22 trains, 32–40/132 cars, 48 Balamb Garden, 49 chocobo, 50 Ragnarok, 64–66 boats. `Wm_ModelIdToVehicleCode`/`Wm_VehicleCodeToModelId` convert between wmset model ids and vehicle codes (chocobo = models 77/78, train = 70, cars = 73–75/81–87, Garden = 1, Ragnarok = 64/65).

* **Boarding** — `World_HandleVehicleBoardingInput`: Cross-button board/disembark with proximity checks, camera-mode toggle, starts the docking state machine (`World_UpdateDockingTransitions`: state 5 Ragnarok landing, 6 Ragnarok board, 7 chocobo dismount camera, 8 Garden descent, 13 Ragnarok map-screen fly-to, 14 train arrival) and boarding music (`World_GetBoardingMusicTrack`).
* **Dismount** — `World_FindDismountPosition` probes 8 directions around the vehicle for a walkable spot (walkability bits, height difference < 200, no blocking entity); failure sets the savemap "vehicle cannot park" flag used by `World_RequestFieldJump`.
* **Steering** — `World_UpdateVehicleSteeringAndCamera` integrates heading/velocity per vehicle class each frame (Ragnarok gets bank + pitch), with chase-camera yaw follow and coordinate wrap-around.
* **Altitude** — `World_ComputeVehicleAltitude`: ground for foot/cars, hover for Garden (ground −128..−256), free flight for Ragnarok (max height 3584, approach ground −200 on landing).
* **Cars consume fuel** — `World_UpdateCarFuelConsumption` decrements one Fuel item (id 0xA2) every 0x20000 distance units and displays "Fuel: N" via the world message-window system; empty tank forces dismount.
* **Trains** — two line structs built by `World_InitTrainLines` from 2048-byte track blocks (16-byte polyline nodes); 3–5 cars of 52 bytes each move along the track (`World_MoveTrainCarAlongTrack`, 30-frame station stops), coupled by cumulative car-length offsets, and are projected/oriented on the walkmesh. Station boarding (`World_UpdateTrainStationBoarding`) costs 3000 gil and runs through the wmset warp script.
* **Chocobo auto-run** — on dismount, a small path VM (`World_ChocoboPathfindStateMachine`) incrementally searches walkable triangles with backtracking, keeps the best path, then replays it to run the chocobo away. The chicobo follower instead replays the player's 16-entry position-history ring with a delay (`World_UpdateFollowerTrail`).

## Rendering scaffolding

`FFWorldInit` sets up double-buffered PSX-style draw/display environments and ordering tables (`World_InitRenderBuffers`), pre-built primitive pools for terrain polys, particles (64+64 slots), ground decals and the sky (gouraud gradient + sun/moon billboards on tpage 45). Per frame: `World_SelectSkyFogParams` (Ragnarok-airborne preset vs default), `World_DrawSkyAndHorizon` (camera-yaw-scrolled sky quads), `World_SpawnVehicleTerrainEffects` (dust/spray/wake/splash per ground type), `World_UpdateAndRenderGroundDecals` (48-byte trail entries projected on the walkmesh).

## Function addresses

| Function | Address | Description |
|---|---|---|
| `World_BuildObjectInstanceList` | 0x544860 | Rebuilds the object instance table on world load |
| `World_SpawnObjectInstance` | 0x545280 | Adds one entry to the object instance table |
| `World_UpdateAndPlaceEntityModels` | 0x5472C0 | Per-frame in-range/position/anim update and draw |
| `World_FindTouchedObject` | 0x548CD0 | Collision/facing scan for touch and script conditions |
| `World_DrawObjectShadow` | 0x54C6C0 | Draws the 2-quad projected object shadow |
| `Wm_ModelIdToVehicleCode` | 0x546F90 | wmset model id to vehicle code |
| `Wm_VehicleCodeToModelId` | 0x546E10 | Vehicle code to wmset model id |
| `World_RestoreParkedVehiclePositions` | 0x54D6A0 | Restores parked vehicle positions on load |
| `World_SaveWorldStateToSavemap` | 0x549E80 | Saves world object/vehicle state to the savemap |
| `World_PlacePlayerAtWarpPoint` | 0x548AF0 | Places the player at a warp point |
| `World_GetVehicleClearanceRadius` | 0x54D9C0 | Vehicle clearance radius (Garden/Ragnarok/cars) |
| `World_GetBoardingMusicTrack` | 0x5447A0 | Boarding music track per vehicle |
| `Wm_MsgWindow_Show/ShowAsk/Close` | 0x543790/0x5438D0/0x543A40 | World message-window open/ask/close |
| `world_object_instances` | 0x20426C0 | Object instance table (global) |
| `World_UpdateVehicleSteeringAndCamera` | 0x557A90 | Per-frame heading/velocity/chase-camera update |
| `World_ComputeVehicleAltitude` | 0x53ECE0 | Ground/hover/flight altitude per vehicle class |
| `World_HandleVehicleBoardingInput` | 0x54A7F0 | Board/disembark input handling |
| `World_UpdateDockingTransitions` | 0x54B460 | Docking state machine |
| `World_FindDismountPosition` | 0x53E7A0 | Probes for a walkable dismount spot |
| `World_UpdateCarFuelConsumption` | 0x54FDA0 | Car fuel decrement and display |
| `World_InitTrainLines` | 0x545330 | Builds train line structs from track blocks |
| `World_MoveTrainCarAlongTrack` | 0x545B20 | Moves a train car along its track |
| `World_UpdateTrainStationBoarding` | 0x5484B0 | Train station boarding sequence |
| `World_ChocoboPathfindStateMachine` | 0x54DCF0 | Chocobo auto-run pathfinding |
| `World_UpdateFollowerTrail` | 0x54DAD0 | Chicobo follower trail replay |
| `World_SpawnVehicleTerrainEffects` | 0x550070 | Dust/spray/wake/splash per ground type |
| `World_UpdateFullMapScreen` | 0x543CB0 | Fullscreen map rendering |
| `world_extra_object_instances` | 0xC76588 | Secondary 4-entry object table (global) |
| `world_msg_windows[13]` | 0xC761A0 | World message-window slot array (global) |
