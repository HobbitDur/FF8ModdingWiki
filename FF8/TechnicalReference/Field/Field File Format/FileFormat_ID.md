---
layout: default
parent: Field File Format
title: Field Walkmesh
permalink: /technical-reference/field/field-file-format/field-walkmesh/
---

1. TOC
{:toc}

# Field walkmesh (`.id`)

Every field has one `.id` file: the walkmesh the player and NPCs walk on. It is a flat list of
3D triangles plus a per-edge neighbour table — no bounding volume, no spatial index, no header
beyond a single count.

The engine does **not parse** this file. `FFFieldDirector` loads it raw and simply points two
globals into the buffer, so the on-disk layout *is* the in-memory layout:

```c
FIELD_WALKMESH_TRIANGLES = idFileBase + 4;
FIELD_WALKMESH_ADJACENCY = FIELD_WALKMESH_TRIANGLES + 24 * *(uint16_t *)idFileBase;
```

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA, image base 0x400000.
Everything below was cross-checked against the 895 `.id` files of the retail PC release.

## File layout

| Offset | Size | Contents |
|---|---|---|
| 0x00 | 4 | `triangleCount` (uint32 LE) |
| 0x04 | `24 × count` | Triangle array |
| `4 + 24×count` | `6 × count` | Access (adjacency) array |

Total size is exactly `4 + 30 × count`. All 895 retail files match this with no exception and
no padding.

{: .note }
Deling also accepts a file that is 2 bytes longer and keeps those trailing bytes as an unknown
value. No PC-release field file has them; it is a PlayStation-disc variant.

### Triangle (24 bytes)

Three vertices, 8 bytes each:

| Offset | Type | Field |
|---|---|---|
| 0x00 | int16 | x |
| 0x02 | int16 | y |
| 0x04 | int16 | z |
| 0x06 | int16 | copy of **vertex 0's** z |

The fourth int16 is not padding and not garbage: in all 455 226 vertices of the retail PC files
it equals the z of the triangle's **first** vertex — including in vertices 1 and 2, which
therefore carry a value unrelated to their own z (that matches only 89.8% of the time). It is
most likely an artefact of how the exporter wrote a 4-word vertex.

**Nothing in the engine ever reads it.** Every walkmesh consumer indexes the triangle as an
`int16[12]` and touches only elements 0-2, 4-6 and 8-10 — verified in `Field_Walkmesh_ResolveMovement`,
`Field_Walkmesh_MoveEntityStep`, `Field_Walkmesh_PlaceEntitiesOnLoad` and
`Field_Walkmesh_HeightOnTriangle`. An editor may write anything there; writing `vertices[0].z`
reproduces the original bytes exactly.

### Access / adjacency (6 bytes)

Three int16, one per edge:

| Index | Edge | Meaning |
|---|---|---|
| 0 | v0 → v1 | Triangle id reached across this edge |
| 1 | v1 → v2 | idem |
| 2 | v2 → v0 | idem |

`-1` means there is no neighbour: the edge is a wall. Any other value is an index into the
triangle array. Across the retail files, all 455 226 entries are either a valid index or `-1` —
never out of range.

## Coordinates

Walkmesh coordinates are plain int16 in field space. x/y are the ground plane (the 2D
containment tests use only those) and z is height.

Entity positions are stored in **12-bit fixed point** (`pos_x / 4096` converts to walkmesh
units), so the mesh has integer resolution but characters move sub-unit.

`current_triangle` in the 612-byte entity struct is a **uint16** index into this array.

## Rules the engine imposes

These are not conventions — break one and the field misbehaves.

### Winding must be consistent

Both the containment test (`Field_Walkmesh_FindTriangleAt`) and the transition test
(`Field_Walkmesh_ResolveMovement`) use the same 2D cross product per edge and treat a
**negative** result as "outside that edge":

```
cross_i = (v[i+1].y - v[i].y) * (px - v[i].x) - (v[i+1].x - v[i].x) * (py - v[i].y)
inside  = cross_0 >= 0 && cross_1 >= 0 && cross_2 >= 0
```

A triangle wound the other way has all three crosses negative at its own centroid: the engine
considers every point outside it, so it can never be entered and `FindTriangleAt` will never
return it. 151 723 of the 151 742 retail triangles satisfy the positive convention.

{: .warning }
The 19 exceptions are retail bugs, not an alternative convention:
`eciway12` (252, 253), `eciway14` (252, 253), `glprefr2` (181-183), `glprefr3` (98, 99),
`glpreo2` (54, 55, 90, 92, 108, 139), `titvout1` (92, 93, 311, 312). Those triangles are dead
geometry in the shipped game.

### Adjacency should be reciprocal

If triangle A names B across one edge, B should name A back — otherwise the player can walk
one way through the seam and not the other. Retail has 379 109 links and exactly **one**
non-reciprocal case: `bgroad_6`, triangle 246 edge 0 points at triangle 23, which does not
point back.

Nothing in the engine enforces this; it just walks whatever the table says.

### The triangle must not be vertical

Height comes from the plane equation, dividing by the z component of the edge cross product:

```c
z = (n.x * (v0.x - px) + n.y * (v0.y - py)) / n.z + v0.z;   // n.z == 0 -> returns 0
```

A triangle whose projection onto the ground plane has zero area makes `n.z` zero and the
entity is teleported to height 0. No retail triangle does this.

### Hard limit: 512 triangles

`FIELD_WALKMESH_BLOCKED_BITS` is a **64-byte** bitfield (cleared with `rep stosd`, ecx = 0x10),
i.e. one bit for triangle ids 0-511. `SCRIPT_IDLOCK` / `SCRIPT_IDUNLOCK` and the wall test in
`Field_Walkmesh_ResolveMovement` index it with no bounds check:

```c
FIELD_WALKMESH_BLOCKED_BITS[id / 8] |= 1 << (id % 8);   // SCRIPT_IDLOCK, no range check
```

The largest retail walkmesh has exactly 512 triangles, so the shipped data sits right on the
limit. Movement itself would keep working past 512 (it indexes the file buffer directly), but
any `IDLOCK`/`IDUNLOCK` on a higher id — and the blocked-bit read on every edge crossing —
walks off the end of the array into neighbouring globals.

There is a second, softer limit: the loader computes the adjacency base from `*(uint16_t *)`
the count field, so only the low 16 bits are used there, while `Field_Walkmesh_FindTriangleAt`
reads the same field as a signed int32. Keep the count under 65536 and the two agree.

## Runtime behaviour

### Blocked triangles

The blocked bitfield is **not** stored in the file. It is zeroed on every field entry and is
driven purely by script:

* `IDLOCK` (opcode 0x1F) sets the bit — the triangle becomes a wall.
* `IDUNLOCK` (opcode 0x20) clears it.

A blocked triangle behaves exactly like a `-1` neighbour: the entity is stopped and gets the
wall-slide hint.

### Movement

`Field_Walkmesh_ResolveMovement` tests the position against the three edges of the current
triangle. Leaving an edge hops to that edge's neighbour and retests, looping until the position
is inside a triangle. If the neighbour is `-1` or blocked, the move is refused and the function
returns ±8 — a facing correction whose sign is `cross(edgeDirection, moveDirection)`. That is
the wall slide; `Field_Walkmesh_MoveEntityStep` applies it for up to 16 iterations (2 for the
player).

Height is recomputed from the plane equation after every accepted move, which is what makes
slopes and stairs smooth without any extra data.

### Spawning

On field entry `Field_Walkmesh_PlaceEntitiesOnLoad` puts the player on the triangle the gateway
asked for (the destination-triangle field of the `.inf` gateway record). Two sentinels:

* destination triangle `0x7FFF` → triangle **0**, with default anims, default move speed and
  collision radius 48.
* destination x `0x7FFF` → the **centroid** of the destination triangle (the plain average of
  the three vertices, per axis).

Every other entity keeps its position and just has its height recomputed on its current triangle.

## Editing checklist

When writing or validating an `.id`:

1. `size == 4 + 30 * count`.
2. Every access entry is `-1` or `0 <= id < count`.
3. Every triangle winds positive (all three centroid cross products > 0).
4. Adjacency is reciprocal, and an edge that names a neighbour actually shares two vertices with it.
5. `count <= 512` if any script in the field uses `IDLOCK`/`IDUNLOCK`, and as a safe rule always.
6. No triangle with zero projected area.
7. The 4th int16 of each vertex should be `vertices[0].z` to match the original files byte for byte.

Editing a walkmesh in isolation is not enough: gateway records in the `.inf` store a destination
**triangle id**, so renumbering or deleting triangles silently breaks field exits into that map.
The same applies to any `IDLOCK`/`IDUNLOCK` argument in the field's `.jsm` script.

## Function and global addresses

| Symbol | Address | Description |
|---|---|---|
| `FFFieldDirector` | 0x471F70 | Field module driver; points the walkmesh globals into the loaded `.id` |
| `Field_Walkmesh_MoveEntityStep` | 0x479C60 | Movement step, slope speed scaling and wall-slide probing |
| `Field_Walkmesh_ResolveMovement` | 0x47A3E0 | Edge tests, triangle transitions, blocked/`-1` wall handling |
| `Field_Walkmesh_HeightOnTriangle` | 0x47A680 | Height from the triangle plane equation |
| `Field_Walkmesh_FindTriangleAt` | 0x477B00 | Point → triangle id search (nearest by height among containing triangles) |
| `Field_Walkmesh_PlaceEntitiesOnLoad` | 0x477C90 | Spawn placement on field entry |
| `SCRIPT_IDLOCK` | 0x51D7F0 | Script opcode 0x1F — sets a triangle's blocked bit |
| `SCRIPT_IDUNLOCK` | 0x51D830 | Script opcode 0x20 — clears it |
| `WALKMESH_DATA_POINTER_ID_FILE` | 0x1CF3D40 | Slot holding the pointer to the raw `.id` buffer |
| `FIELD_WALKMESH_TRIANGLES` | 0x1CF3D68 | `.id` + 4 — the triangle array |
| `FIELD_WALKMESH_ADJACENCY` | 0x1CF3D88 | `.id` + 4 + 24×count — the access array |
| `FIELD_WALKMESH_BLOCKED_BITS` | 0x1CE4918 | 64-byte script-driven blocked bitfield (512 triangles) |

## See also

* [Field rendering and collision runtime]({{ site.baseurl }}/technical-reference/field/rendering-collision/)
  — the per-frame view of movement, triggers and gateways.
* [Field gateways]({{ site.baseurl }}/technical-reference/field/field-file-format/field-gateways/)
  — the `.inf` gateway records that reference walkmesh triangle ids.
