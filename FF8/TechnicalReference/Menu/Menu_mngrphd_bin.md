---
layout: default
parent: Menu
title: Mngrphd.bin File Format
permalink: /technical-reference/menu/mngrphdbin-file-format/
---

This is the map for [Mngrp.bin](../mngrpbin-file-format/). Locations to data and the size of the section.

Useless entry (with size = 0 or seek = 0xFF) need to be kept or the game crash.

There is 255 sections with 117 useful section.

## Entry

| Type   | Size | Value | Description                                                                                                                                                                    |
|--------|------|-------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UInt32 | 4    | Seek  | Location of data. This value is **1 more** than the actual location. So may want to **subtract 1** from these values when reading file. (**{0xFFFFFFFF}** values are invalid.) |
| UInt32 | 4    | Size  | Total Size of all data at this location. (**{0x00000000}** values are invalid.)                                                                                                |
