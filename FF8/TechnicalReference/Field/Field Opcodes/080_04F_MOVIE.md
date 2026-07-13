---
layout: default
parent: Field Opcodes
title: 04F_MOVIE
nav_order: 80
permalink: /technical-reference/field/field-opcodes/04f-movie/
---

-   Opcode: **0x04F**
-   Short name: **MOVIE**
-   Long name: Play movie

#### Argument

none

#### Stack

none

#### Description

Plays an FMV movie prepared by [MOVIEREADY](../0a3-movieready/). Waits (return 1) until the movie subsystem is ready, then starts playback (`start_movie`). No stack use.

PC handler: `SCRIPT_MOVIE` at 0x51F390.
