---
layout: default
title: Rinoa combine limit break
nav_order: 27
parent: Kernel
permalink: /technical-reference/main/kernel/rinoa-combine-limit-break/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4A6C | 5        | 20 bytes     |


## Sections

| Offset | Ability         |
|--------|-----------------|
| 0x4A6C | Angelo Cannon   |
| 0x4A80 | Angelo Strike   |
| 0x4A94 | Invincible Moon |
| 0x4AA8 | Wishing Star    |
| 0x4ABC | Angel Wing      |


## Section Structure

| Offset | Length  | Description               |
|--------|---------|---------------------------|
| 0x0000 | 2 bytes | Offset to limit  name     |
| 0x0002 | 2 bytes | Magic ID                  |
| 0x0004 | 1 byte  | Attack type               |
| 0x0005 | 1 byte  | Attack power              |
| 0x0006 | 1 byte  | Attack flags              |
| 0x0007 | 1 byte  | Padding (unused; IDA: 0 xrefs) |
| 0x0008 | 1 byte  | Target info               |
| 0x0009 | 1 byte  | Attack flags — low 2 bits stored as last-attacker flag (`ATTACK_FLAG`); Combine swaps the flags/animation byte order vs other command types |
| 0x000A | 1 byte  | Hit Count                 |
| 0x000B | 1 byte  | Element Attack            |
| 0x000C | 1 byte  | Element Attack %          |
| 0x000D | 1 byte  | Status Attack Enabler     |
| 0x000E | 2 bytes | status_0; //statuses 0-7  |
| 0x0010 | 4 bytes | status_1; //statuses 8-39 |
