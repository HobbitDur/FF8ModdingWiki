---
layout: default
parent: Menu
title: mmagic.bin file format
permalink: /technical-reference/menu/mmagic/
author: hobbitdur, Nihil
---

This file contains 4 bytes for each magic, if the first byte is positive the magic can be used in the menu.  
If the first byte is 0x03, the magic can be used on alive allies, if it's 0x23 it can be used on dead allies.  
The other 3 bytes seem to always be set to 0xFF 0xFF 0x00.  