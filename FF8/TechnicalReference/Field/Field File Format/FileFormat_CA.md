---
layout: default
parent: Field File Format
title: Field Camera
permalink: /technical-reference/field/field-file-format/field-camera/
---

By myst6re.

## Camera

The format is almost the same as Final Fantasy VII. Differences:

-   The zoom can be present twice
-   There may be several cameras, in this case the camera structure is repeated several times, and sizeof(each struct) = 0x28 (with zoom twice for each)

### Structure

| Offset | Size         | Data                                                         |
|--------|--------------|--------------------------------------------------------------|
| 0x00   | 3 × int16    | Camera X axis (4096 = 1.0)                                   |
| 0x06   | 3 × int16    | Camera Y axis                                                |
| 0x0C   | 3 × int16    | Camera Z axis                                                |
| 0x12   | int16        | Copy of the Z axis' z                                        |
| 0x14   | 3 × int32    | Translation                                                  |
| 0x20   | 4 bytes      | Unused                                                       |
| 0x24   | uint16       | Zoom                                                         |
| 0x26   | uint16       | Zoom again (only in the 0x28-byte multi-camera layout)       |

### Projecting a field position onto the background

A field position `P` (walkmesh / SET3 coordinates) goes to camera space with the axes as the
rows of a rotation matrix, then to the screen with the zoom as the projection distance:

```
C = (axes / 4096) · P + translation
screen_x = C.x × zoom / C.z
screen_y = C.y × zoom / C.z
```

The screen position is relative to the background's origin, the point where the
[tiles](FileFormat_MAP) X and Y are 0. Projecting the whole walkmesh of `bghall_1` this way
draws it exactly over the floor, stairs and bridge of the background.
