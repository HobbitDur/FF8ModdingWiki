---
layout: default
title: Slot array
nav_order: 28
parent: Kernel
permalink: /technical-reference/main/kernel/slot-array/
---


## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4AD0 | 60       | 1 byte       |


## Sections

| Offset | Ability       |
|--------|---------------|
| 0x4AD0 | Slot array 1  |
| 0x4AD1 | Slot array 2  |
| 0x4AD2 | Slot array 3  |
| 0x4AD3 | Slot array 4  |
| 0x4AD4 | Slot array 5  |
| 0x4AD5 | Slot array 6  |
| 0x4AD6 | Slot array 7  |
| 0x4AD7 | Slot array 8  |
| 0x4AD8 | Slot array 9  |
| 0x4AD9 | Slot array 10 |
| 0x4ADA | Slot array 11 |
| 0x4ADB | Slot array 12 |
| 0x4ADC | Slot array 13 |
| 0x4ADD | Slot array 14 |
| 0x4ADE | Slot array 15 |
| 0x4ADF | Slot array 16 |
| 0x4AE0 | Slot array 17 |
| 0x4AE1 | Slot array 18 |
| 0x4AE2 | Slot array 19 |
| 0x4AE3 | Slot array 20 |
| 0x4AE4 | Slot array 21 |
| 0x4AE5 | Slot array 22 |
| 0x4AE6 | Slot array 23 |
| 0x4AE7 | Slot array 24 |
| 0x4AE8 | Slot array 25 |
| 0x4AE9 | Slot array 26 |
| 0x4AEA | Slot array 27 |
| 0x4AEB | Slot array 28 |
| 0x4AEC | Slot array 29 |
| 0x4AED | Slot array 30 |
| 0x4AEE | Slot array 31 |
| 0x4AEF | Slot array 32 |
| 0x4AF0 | Slot array 33 |
| 0x4AF1 | Slot array 34 |
| 0x4AF2 | Slot array 35 |
| 0x4AF3 | Slot array 36 |
| 0x4AF4 | Slot array 37 |
| 0x4AF5 | Slot array 38 |
| 0x4AF6 | Slot array 39 |
| 0x4AF7 | Slot array 40 |
| 0x4AF8 | Slot array 41 |
| 0x4AF9 | Slot array 42 |
| 0x4AFA | Slot array 43 |
| 0x4AFB | Slot array 44 |
| 0x4AFC | Slot array 45 |
| 0x4AFD | Slot array 46 |
| 0x4AFE | Slot array 47 |
| 0x4AFF | Slot array 48 |
| 0x4B00 | Slot array 49 |
| 0x4B01 | Slot array 50 |
| 0x4B02 | Slot array 51 |
| 0x4B03 | Slot array 52 |
| 0x4B04 | Slot array 53 |
| 0x4B05 | Slot array 54 |
| 0x4B06 | Slot array 55 |
| 0x4B07 | Slot array 56 |
| 0x4B08 | Slot array 57 |
| 0x4B09 | Slot array 58 |
| 0x4B0A | Slot array 59 |
| 0x4B0B | Slot array 60 |


## Section Structure

| Offset | Length | Description |
|--------|--------|-------------|
| 0x0000 | 1 byte | Slot Set ID — index (0-15) into the [Selphie limit-break sets]({{site.baseurl}}/technical-reference/main/kernel/slot-sets/) (kernel section 28), which holds 16 sets of 8 magic/count pairs. This section only stores which set to roll; what each set actually contains is a separate section |