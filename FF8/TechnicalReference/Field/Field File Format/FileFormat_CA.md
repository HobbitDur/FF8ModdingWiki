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
