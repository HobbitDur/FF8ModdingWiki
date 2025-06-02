---
layout: default
title: Memory info
parent: ExeData
author: HobbitDur
permalink: /technical-reference/exedata/memory-info/
---

1. TOC
{:toc}

## Notes

BCI seems to stand for BattleCharacterInfo
To find the size, I take the slot 0 size
BCI_CURRENT_HP is at 1D27B28, and next slot data is at 1D27BF8, so data size is 208.
So to get a specific value of a specific slot ID, we takes the first value then shift by 208.

The data order:

| Data name      | Size |
|----------------|------|
| BCI_CURRENT_HP | 4    |
| BCI_MAX_HP     | 4    |

| BCI_LVL     | 1    |
| BCI_STR     | 1    |
| BCI_VIT     | 1    |
| BCI_MAG     | 1    |
| BCI_SPR     | 1    |
| BCI_SPD     | 1    |
| BCI_LUCK     | 1    |
| BCI_EVA     | 1    |
| BCI_HIT     | 1    |

In this website (https://github.com/ff8-speedruns/ff8-memory), Level of ally 1 is at FF8_EN.exe+1927BCC, when the BCI_LVL is at 1D27BCC  
If you do the +0x400000 of FF8_EN.exe it checks out. So we can use this existing mapping.


struct BciTimerStruct
{
  0: Sleep
  1: Haste
  2: Slow
  3: Stop
  4: Regen
  5: Protect
  6: Shell
  7: Reflect
  8: Aura
  9: Curse
  10:Doom
  11:Hero
  12:Petrify
  13:Float
  14:Unknown14
  15:Unknown15
};
01D27B64
1CFF574


