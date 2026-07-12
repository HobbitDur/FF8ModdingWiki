---
title: Section 2 - Model geometry
layout: default
parent: Monster files (c0mxxx.dat)
permalink: /technical-reference/battle/monster-files-c0mxxxdat/section-2-model-geometry/
nav_order: 2
---

## Section 2: Model geometry

### Header (data sub table)

| Offset             | Length               | Description             |
|--------------------|----------------------|--------------------------|
| 0                  | 4 bytes              | Number of objects       |
| 4                  | nbObjects \* 4 bytes | Object Positions        |
| 4 + nbObjects \* 4 | Varies               | Object Data (see below) |
| Varies             | 4 bytes              | Total count of vertices |

### Object Data

| Offset | Length                     | Description               |
|--------|----------------------------|----------------------------|
| 0      | 2 bytes                    | Number of Vertices Data   |
| 2      | Varies \* NbVerticesData   | Vertices Data (see below) |
| Varies | 4 - (absolutePosition % 4) | Padding (0x00)            |
| Varies | 2 bytes                    | Num triangles             |
| Varies | 2 bytes                    | Num quads                 |
| Varies | 8 bytes                    | Always empty              |
| Varies | numTriangles \* 16 bytes   | Triangles                 |
| Varies | numQuads \* 20 bytes       | Quads                     |

#### Vertice Data

| Offset | Length                | Description                       |
|--------|-----------------------|------------------------------------|
| 0      | 2 bytes               | Bone id                           |
| 2      | 2 bytes               | Number of vertices                |
| 4      | nbVertices \* 6 bytes | Vertices (nbVertices \* 3 shorts) |

#### Useful structures

```
struct vertice {  
     sint16    x, y, z;  
};
```

(sizeof = 6)

```
struct triangle {  
     uint16    vertex_indexes[3]; // vertex_indexes[0] &= 0xFFF, other bits are unknown  
     uint8 texCoords1[2];  
     uint8 texCoords2[2];  
     uint16    textureID_related;  
     uint8 texCoords3[2];  
     uint16    u; // textureID_related2  
};
```

(sizeof = 16)

```
struct quad {  
     uint16    vertex_indexes[4]; // vertex_indexes[0] &= 0xFFF, other bits are unknown  
     uint8 texCoords1[2];  
     uint16    textureID_related;  
     uint8 texCoords2[2];  
     uint16    u; // textureID_related2  
     uint8 texCoords3[2];  
     uint8 texCoords4[2];  
};
```

(sizeof = 20)
