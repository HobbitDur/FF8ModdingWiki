---
layout: default
title: Rinoa commands
nav_order: 26
parent: Kernel
permalink: /technicalreference/main/kernel/rinoa-commands/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4A5C | 2        | 8 bytes      |

## Sections

| Offset | Ability    |
|--------|------------|
| 0x4A5C | Angelo     |
| 0x4A64 | Angel Wing |

## Section Structure

| Offset | Length  | Description                   |
|--------|---------|-------------------------------|
| 0x0000 | 2 bytes | Offset to ability name        |
| 0x0002 | 2 bytes | Offset to ability description |
| 0x0004 | 1 byte  | Unknown Flags                 |
| 0x0005 | 1 byte  | Target                        |
| 0x0006 | 1 byte  | Ability data ID               |
| 0x0007 | 1 byte  | Unknown / Unused              |
