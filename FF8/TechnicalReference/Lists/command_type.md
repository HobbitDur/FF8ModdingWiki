---
layout: default
title: Command type
parent: List
author: hobbitdur, nihil
permalink: /technical-reference/list/command-type/
---

Check means condition check in AI

| ID (Dec) | ID (Hex) | Data                    | Comment                                                                              |
|----------|----------|-------------------------|--------------------------------------------------------------------------------------|
| 0        | 0x00     | Kamikaze/Phoenix Pinion | Command failed can't actually be checked for                                         |
| 1        | 0x01     | Attack                  | becomes 253 on hit for gunblade users, but this can't be checked for                 |
| 2        | 0x02     | Magic                   |                                                                                      |
| 4        | 0x04     | Item                    |                                                                                      |
| 5        | 0x05     | Renzokuken without finisher                    |                                                                                      |
| 6        | 0x06     | Draw                    |                                                                                      |
| 7        | 0x07     | Devour                  | becomes 0 if it fails, but this can't be checked for                                 |
| 8        | 0x08     | Monster Attack          |                                                                                      |
| 12       | 0x0C     | Mug                     |                                                                                      |
| 14       | 0x0E     | Shot                    | becomes 237 on hit, 238 when time expires, but these can't be checked for            |
| 15       | 0x0F     | Blue Magic              |                                                                                      |
| 16       | 0x10     | Slot                    |                                                                                      |
| 17       | 0x11     | No Mercy                |                                                                                      |
| 18       | 0x12     | Sorcery                 |                                                                                      |
| 19       | 0x13     | Combine                 |                                                                                      |
| 23       | 0x17     | Defend                  |                                                                                      |
| 24       | 0x18     | Mad Rush                |                                                                                      |
| 25       | 0x19     | Treatment               |                                                                                      |
| 26       | 0x1A     | Recover                 |                                                                                      |
| 27       | 0x1B     | Revive                  |                                                                                      |
| 28       | 0x1C     | Darkside                | becomes 243 on hit for gunblade users, and 0 on kill, but these can't be checked for |
| 29       | 0x1D     | Card                    | becomes 0 if it fails, but this can't be checked for                                 |
| 30       | 0x1E     | Doom                    | becomes 246 when timer reaches 0, but this can't be checked for                      |
| 32       | 0x20     | Absorb                  |                                                                                      |
| 33       | 0x21     | LV Down                 | becomes 0 if it fails, but this can't be checked for                                 |
| 34       | 0x22     | LV Up                   | becomes 0 if it fails, but this can't be checked for                                 |
| 38       | 0x26     | MiniMog                 | becomes 0 if MiniMog is not available, but this can't be checked for                 |
| 237      | 0xED     | Shot on hit             |                                                                                      |
| 238      | 0xEE     | Shot time expire        |                                                                                      |
| 240      | 0xF0     | Angelo Automove         |                                                                                      |
| 241      | 0xF1     | Duel                    |                                                                                      |
| 243      | 0xF3     | Darkside gunblade       |                                                                                      |
| 244      | 0xF4     | Chocobo                 |                                                                                      |
| 245      | 0xF5     | Odin/Gilgamesh          |                                                                                      |
| 246      | 0xF6     | Doom finished           |                                                                                      |
| 249      | 0xF9     | Renzokuken finisher     |                                                                                      |
| 250      | 0xFA     | Renzokuken              | becomes 251 on hit and 249 on finisher use, but these can't be checked for           |
| 251      | 0xFB     | Renzokuken on hit       |                                                                                      |
| 252      | 0xFC     | Special action          |                                                                                      |
| 253      | 0xFD     | Gunblade on hit         |                                                                                      |
| 254      | 0xFE     | G-Force                 |                                                                                      |
