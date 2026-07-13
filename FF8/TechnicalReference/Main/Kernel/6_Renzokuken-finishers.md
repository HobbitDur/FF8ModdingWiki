---
layout: default
title: Renzokuken finishers
nav_order: 7
parent: Kernel
permalink: /technical-reference/main/kernel/renzokuken-finishers/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x3744 | 4        | 24 bytes     |

## Sections

| Offset | Limit         |
|--------|---------------|
| 0x3744 | Rough Divide  |
| 0x375C | Fated Circle  |
| 0x3774 | Blasting Zone |
| 0x378C | Lion Heart    |

## Section Structure

| Offset | Length  | Description                 |
|--------|---------|-----------------------------|
| 0x0000 | 2 bytes | Offset to limit name        |
| 0x0002 | 2 bytes | Offset to limit description |
| 0x0004 | 2 bytes | Magic ID                    |
| 0x0006 | 1 byte  | Attack Type                 |
| 0x0007 | 1 byte  | Padding (unused; IDA: 0 xrefs) |
| 0x0008 | 1 byte  | Attack power                |
| 0x0009 | 1 byte  | Target hit/reaction animation ID (`HIT_TYPE_TARGET_ANIMATION_TO_PLAY`) played on the target when the ability lands |
| 0x000A | 1 byte  | Target info                 |
| 0x000B | 1 byte  | Attack Flags                |
| 0x000C | 1 byte  | Hit count                   |
| 0x000D | 1 byte  | Element Attack              |
| 0x000E | 1 byte  | Element Attack %            |
| 0x000F | 1 byte  | Status Attack Enabler       |
| 0x0010 | 2 bytes | Padding (unused; IDA: 0 xrefs) |
| 0x0012 | 2 bytes | status_0; //statuses 0-7    |
| 0x0014 | 4 bytes | status_1; //statuses 8-39   |
