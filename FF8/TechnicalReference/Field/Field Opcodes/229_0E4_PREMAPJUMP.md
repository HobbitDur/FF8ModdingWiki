---
layout: default
parent: Field Opcodes
title: 0E4_PREMAPJUMP
nav_order: 229
author: HobbitDur
permalink: /technical-reference/field/field-opcodes/0e4-premapjump/
---

-   Opcode: **0x0E4**
-   Short name: **PREMAPJUMP**
-   Long name: Declare a scripted exit

#### Argument

none

#### Stack


*Field Map ID*

*XCoord*

*YCoord*

*ZCoord*

**PREMAPJUMP**

#### Description

Declares where a scripted exit leads, without jumping. On PC it has no effect on the game.

The handler looks for the first free record in the [gateway table](../../field-file-format/field-gateways/) of the `.inf` loaded in memory (field ID 0x7FFF) and writes:

| Gateway value          | Written value                 |
|------------------------|-------------------------------|
| Exit line point 1 X    | *XCoord*                      |
| Exit line point 1 Y    | *YCoord*                      |
| Exit line point 1 Z    | *ZCoord*                      |
| Destination triangle   | -1                            |
| Destination field ID   | *Field Map ID*                |
| Next record's field ID | 0x7FFF (the new end of table) |

The rest of the record keeps its old content. The opcode then continues with the next instruction (returns 2).

The record never fires: `Field_Collision_CheckGatewayCrossing` skips any gateway with triangle -1. Its only reader is `Field_Collision_FindNearestGatewayDest`, which runs every frame and stores the field ID of the gateway nearest to the player in `FIELD_NEAREST_GATEWAY_FIELD_ID`. Nothing in the PC executable reads that variable. The name and this "nearest exit" lookup suggest a hint for reading the next field ahead of time, but no such code exists on PC.

#### Use in the scripts

The retail scripts use it 790 times, in 252 fields. 757 of those are in line entities, 289 of them after a `SETLINE` in the same script. The destination usually matches a map jump in the same entity, so the script is declaring where its own exit leads.

| Destination                            | Uses |
|----------------------------------------|------|
| Same as a map jump of the same entity  | 702  |
| Same as a map jump of another entity   | 45   |
| Below 72 (world map, as for a gateway) | 38   |
| Neither                                | 5    |

#### Modding

The search for a free record has no limit. If the gateways of a field and its executed PREMAPJUMP total more than 12, the handler writes past the table into the door triggers and beyond. With 12 in total, the end marker alone lands on the Y of trigger 1's first corner. The highest retail total is 10 (`feart1f1` and `bghall_1`), counting one PREMAPJUMP per entity.

Records last until the next field load, because the `.inf` is reloaded.

PC handler: `SCRIPT_PREMAPJUMP`.

## Function addresses

| Function                                 | Address   | Description                                   |
|------------------------------------------|-----------|-----------------------------------------------|
| `SCRIPT_PREMAPJUMP`                      | 0x521960  | Field script opcode handler                   |
| `Field_Collision_FindNearestGatewayDest` | 0x47BD20  | Finds the nearest gateway each frame          |
| `Field_Collision_CheckGatewayCrossing`   | 0x477980  | Fires gateways, skips triangle -1             |
| `FIELD_NEAREST_GATEWAY_FIELD_ID`         | 0x1CDC6E8 | Global variable, written and never read       |
| `FIELD_INF_DATA_PTR`                     | 0x1CDC744 | Global variable, pointer to the loaded `.inf` |
