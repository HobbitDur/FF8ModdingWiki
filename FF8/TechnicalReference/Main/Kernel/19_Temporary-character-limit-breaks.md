---
layout: default
title: Temporary characters limit breaks
nav_order: 20
parent: Kernel
permalink: /technical-reference/main/kernel/temporary-characters-limit-breaks/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4480 | 5        | 24 bytes     |

## Sections

| Offset | Ability        |
|--------|----------------|
| 0x4480 | No Mercy       |
| 0x4498 | Ice Strike     |
| 0x44B0 | Desperado      |
| 0x44C8 | Blood Pain     |
| 0x44E0 | Massive Anchor |

## Section Structure

| Offset | Length  | Description                 |
|--------|---------|-----------------------------|
| 0x0000 | 2 bytes | Offset to limit name        |
| 0x0002 | 2 bytes | Offset to limit description |
| 0x0004 | 2 bytes | Magic ID                    |
| 0x0006 | 1 byte  | Attack Type                 |
| 0x0007 | 1 byte  | Attack Power                |
| 0x0008 | 1 byte  | Target hit/reaction animation index (`HIT_TYPE_TARGET_ANIMATION_TO_PLAY`) played on the target when the ability lands — retail entries use `4`/`5`. (This byte and 0x09 were previously documented as one WORD holding `0x8004`/`0x8005` with an "inert" high byte — the high byte is actually the separate field below) |
| 0x0009 | 1 byte  | [Status window flags]({{site.baseurl}}/technical-reference/list/battle/#status-window-flags) — all retail entries use `0x80` (ally status panel hidden while targeting); `BuildLimitCommandMenu` reads it (as `HIBYTE` of the old WORD) into the Seifer/Edea limit list entry's status-window slot |
| 0x000A | 1 byte  | Target Info                 |
| 0x000B | 1 byte  | Attack Flags                |
| 0x000C | 1 byte  | Hit Count                   |
| 0x000D | 1 byte  | Element Attack              |
| 0x000E | 1 byte  | Element Attack %            |
| 0x000F | 1 byte  | Status attack accuracy       |
| 0x0010 | 2 bytes | [Status 1]({{site.baseurl}}/technical-reference/list/status-flags#status-1) (statuses 0-15)    |
| 0x0012 | 2 bytes | Padding (unused; IDA: 0 xrefs) |
| 0x0014 | 4 bytes | [Status 2]({{site.baseurl}}/technical-reference/list/status-flags#status-2) (statuses 16-47)   |
