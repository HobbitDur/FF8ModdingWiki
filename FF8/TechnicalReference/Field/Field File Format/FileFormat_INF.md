---
layout: default
parent: Field File Format
title: Field Gateways
permalink: /technical-reference/field/field-file-format/field-gateways/
---

By myst6re.

# Gateways/Triggers

| Offset | Size     | Data                                                                                  |
|--------|----------|---------------------------------------------------------------------------------------|
| 0      | 9        | Name of field (\\0 terminated)                                                        |
| 9      | 1        | Control Direction                                                                     |
| 10     | 6        | Unknown                                                                               |
| 16     | 2        | Like \[PVP\] value (was a link, target page no longer exists)                                   |
| 18     | 2        | Height to focus the camera on the character (0= Focus on the feet, 200= normal focus) |
| 20     | 8\*8     | Camera Ranges                                                                         |
| 84     | 2\*8     | Screen Ranges                                                                         |
| 100    | 32 \* 12 | Gateways                                                                              |
| 484    | 16 \* 12 | Triggers                                                                              |

## Range data

Gives the limits of the camera when moving.

`typedef struct {`  
`   qint16 top;`  
`   qint16 bottom;`  
`   qint16 right;`  
`   qint16 left;`  
`} Range;`

### Camera Range

Each range corresponds to a background layer.

### Screen Range

Always (0, 224, 320, 0) twice. The first range change the screen resolution, the second seems to do nothing.

## Gateways data

Passage between fields (the exits the player walks through). There are always 12 records; unused ones have field ID 0x7FFF.  
For each gateway (32 bytes, all values little-endian):

| Offset | Size   | Data                                                                                     |
|--------|--------|------------------------------------------------------------------------------------------|
| 0      | 2 \* 3 | Exit line point 1: X, Y, Z (int16)                                                        |
| 6      | 2 \* 3 | Exit line point 2: X, Y, Z (int16)                                                        |
| 12     | 2      | Destination X (int16)                                                                    |
| 14     | 2      | Destination Y (int16)                                                                    |
| 16     | 2      | Destination walkmesh triangle ID, in the **destination** field's `.id` (int16)            |
| 18     | 2      | Destination field ID (0x7FFF = unused gateway; below 0x48 = world map, see below)          |
| 20     | 2 \* 4 | Unknown, not read by the gateway test (usually 0; 0x7FFF, 0xFF... in a few fields)        |
| 28     | 1      | Facing direction on arrival (0–255 angle units)                                          |
| 29     | 3      | Copies of byte 28 in 1595 of the 1632 used gateways; not read by the gateway test          |

"Destination vertex" in older documents is really X, Y and the triangle ID: there is no destination Z, because the height comes from the triangle.

### How a gateway fires

`Field_Collision_CheckGatewayCrossing` (FF8_EN.exe 0x477980) runs for the player entity after each move. For every gateway whose field ID is not 0x7FFF, it checks two things, using only X and Y (the Z values of the exit line are ignored):

1. The player is within touch range of the exit line **segment** (`Field_Collision_PointToLineDistSq`, squared distance compared with the squared touch radius of the entity).
2. The player's position has changed side of the line between the previous and the current frame (the sign of the cross product flips).

When both are true, the game copies the record into the jump globals, exactly like the [MAPJUMP](../../field-opcodes/029-mapjump/) opcode:

| Gateway value | Global | Used on arrival as |
|---|---|---|
| Destination field ID | `MenuState_opcode_menu_id` | New `CURRENT_FIELD_ID` (the line number in `maplist`) |
| Destination X / Y | `wm2field_FieldX` / `wm2field_FieldY` | Spawn position |
| Destination triangle | `wm2field_FieldZ` | Spawn walkmesh triangle (the height is computed from it) |
| Byte 28 | `wm2field_FieldTarget` | Facing direction |

A field ID below 0x48 selects the world map module (`globalFieldNextModuleID` = 7) instead of the field module (1).

Because the destination triangle is an index into another field's walkmesh, removing or reordering triangles in a `.id` file can break the gateways of every field that leads to it (and the `MAPJUMP` opcodes that target it).

Across the 893 retail `.inf` files, 1632 gateways are used and 9084 are disabled by field ID 0x7FFF.

## Triggers data

Doors interactions.  
For each trigger:

| Offset | Size | Data              |
|--------|------|-------------------|
| 0      | 6    | Vertex of corner1 |
| 6      | 6    | Vertex of corner2 |
| 12     | 1    | Door ID (or 0xFF) |
| 13     | 3    | *Blank*           |

## Function addresses

| Function | Address | Description |
|---|---|---|
| `Field_Collision_CheckGatewayCrossing` | 0x477980 | Tests the 12 gateways against the player's move and starts the jump |
| `Field_Collision_PointToLineDistSq` | 0x4774A0 | Squared distance from a point to a segment (touch range test) |
| `Field_Walkmesh_PlaceEntitiesOnLoad` | 0x477C90 | Places the party on the destination triangle when the new field loads |

Addresses are for FF8_EN.exe (2000 PC release), image base 0x400000.

# Old formats

In the PC version, you can sometimes see older versions of this format, there are three that are more similar to the format of Final Fantasy VII.

## 672 bytes format

The first Unknown data are 4 bytes and there is no PVP field.

## 576 bytes format

Same as 672 bytes format + the first Unknown data in Gateways are not present (like FF7).

## 504 bytes format

Same as 576 bytes format + There is only one camera range and no screen range.
