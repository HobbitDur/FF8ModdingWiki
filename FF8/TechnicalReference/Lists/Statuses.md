---
layout: default
title: Status flags
parent: List
permalink: /technical-reference/list/status-flags/
---

# Status 1

| bit index | Flag   | Description |
|-----------|--------|-------------|
| 0         | 0x0001 | Death       | 
| 1         | 0x0002 | Poison      |
| 2         | 0x0004 | Petrify     |
| 3         | 0x0008 | Darkness    |
| 4         | 0x0010 | Silence     |
| 5         | 0x0020 | Berserk     |
| 6         | 0x0040 | Zombie      |
| 7         | 0x0080 | Unused      |
| 8         | 0x0100 | HP < 25%    |
| 9         | 0x0200 | HP < 50%    |
| 10        | 0x0400 | Unused      |
| 11        | 0x0800 | Unused      |
| 12        | 0x1000 | Unused      |
| 13        | 0x2000 | Unused      |
| 14        | 0x4000 | Unused      |
| 15        | 0x8000 | Unused      |             


# Status 2

| bit index | Flag       | Description            |
|-----------|------------|------------------------|
| 0         | 0x00000001 | Sleep                  |
| 1         | 0x00000002 | Haste                  |
| 2         | 0x00000004 | Slow                   |
| 3         | 0x00000008 | Stop                   |
| 4         | 0x00000010 | Regen                  |
| 5         | 0x00000020 | Protect                |
| 6         | 0x00000040 | Shell                  |
| 7         | 0x00000080 | Reflect                |
| 8         | 0x00000100 | Aura                   |
| 9         | 0x00000200 | Curse                  |
| 10        | 0x00000400 | Doom                   |
| 11        | 0x00000800 | Invincible             |
| 12        | 0x00001000 | Gradual petrify        |
| 13        | 0x00002000 | Float                  |
| 14        | 0x00004000 | Confusion              |
| 15        | 0x00008000 | Drain                  |
| 16        | 0x00010000 | Eject                  |
| 17        | 0x00020000 | Double                 |
| 18        | 0x00040000 | Triple                 |
| 19        | 0x00080000 | Defend                 |
| 20        | 0x00100000 | Immune Physical attack |
| 21        | 0x00200000 | Immune Magic attack    |
| 22        | 0x00400000 | Charged                |
| 23        | 0x00800000 | Back attack            |
| 24        | 0x01000000 | Vit0                   |
| 25        | 0x02000000 | Angel Wing             |
| 26        | 0x04000000 | Unused — no name in the IDB and no reference in the battle status pipeline (`applyDamageAndHandleDeath`, `ComputeMagicAndGFDamage`, `removeStatus`, ...) |
| 27        | 0x08000000 | Unused — as above |
| 28        | 0x10000000 | Unused — as above |
| 29        | 0x20000000 | Unused — as above |
| 30        | 0x40000000 | Has Magic (`STATUS2_HAS_MAGIC`) |
| 31        | 0x80000000 | Summon GF in progress / invocation pending — set as `status_2 \|= STATUS2_SUMMON_GF` while a GF summon plays; checked via `SLOBYTE(status_2) < 0` |

# Ai status

| ID  | Hex    | Name                          |
|-----|--------|-------------------------------|
| 0   | 0x00   | Death                         |
| 1   | 0x01   | Poison                        |
| 2   | 0x02   | Petrify                       |
| 3   | 0x03   | Blind                         |
| 4   | 0x04   | Silence                       |
| 5   | 0x05   | Berserk                       |
| 6   | 0x06   | Zombie                        |
| 7   | 0x07   | Unknown                       |
| 8   | 0x08   | HP < 25%                      |
| 9   | 0x09   | HP < 50%                      |
| 10  | 0x0A   | Unknown                       |
| 11  | 0x0B   | Unknown                       |
| 12  | 0x0C   | Unknown                       |
| 13  | 0x0D   | Unknown                       |
| 14  | 0x0E   | Unknown                       |
| 15  | 0x0F   | Unknown                       |
| 16  | 0x10   | Sleep                         |
| 17  | 0x11   | Haste                         |
| 18  | 0x12   | Slow                          |
| 19  | 0x13   | Stop                          |
| 20  | 0x14   | Regen                         |
| 21  | 0x15   | Protect                       |
| 22  | 0x16   | Shell                         |
| 23  | 0x17   | Reflect                       |
| 24  | 0x18   | Aura                          |
| 25  | 0x19   | Curse                         |
| 26  | 0x1A   | Doom                          |
| 27  | 0x1B   | Invincible                    |
| 28  | 0x1C   | Petrifying                    |
| 29  | 0x1D   | Float                         |
| 30  | 0x1E   | Confuse                       |
| 31  | 0x1F   | Drain                         |
| 32  | 0x20   | Eject                         |
| 33  | 0x21   | Double                        |
| 34  | 0x22   | Triple                        |
| 35  | 0x23   | Defend                        |
| 36  | 0x24   | Immune Physical attack        |
| 37  | 0x25   | Immune Magic attack           |
| 38  | 0x26   | Charged                       |
| 39  | 0x27   | Back Attack                   |
| 40  | 0x28   | VIT 0                         |
| 41  | 0x29   | Angel Wing                    |
| 42  | 0x2A   | Zantetsuken?                  |
| 43  | 0x2B   | Unknown                       |
| 44  | 0x2C   | Unknown                       |
| 45  | 0x2D   | Unknown                       |
| 46  | 0x2E   | Has magic                     |
| 47  | 0x2F   | Invocation pending            |
| 200 | 0xC8   | Male                          |
| 201 | 0xC9   | Female                        |
| 203 | 0xCB   | Highest HP                    |
| 204 | 0xCC   | Lowest HP                     |
| 205 | 0xCD   | Highest Strength              |
| 206 | 0xCE   | Highest Defense               |
| 207 | 0xCF   | Highest Magic                 |
| 208 | 0xD0   | Highest Spirit                |
| 209 | 0xD1   | Highest Speed                 |
| 210 | 0xD2   | Highest Luck                  |
| 211 | 0xD3   | Highest Evade                 |
| 212 | 0xD4   | Highest Hit                   |
| 213 | 0xD5   | Lowest Strength               |
| 214 | 0xD6   | Lowest Vitality               |
| 215 | 0xD7   | Lowest Magic                  |
| 216 | 0xD8   | Lowest Spirit                 |
| 217 | 0xD9   | Lowest Speed                  |
| 218 | 0xDA   | Lowest Luck                   |
| 219 | 0xDB   | Lowest Evade                  |
| 220 | 0xDC   | Lowest Hit                    |
| 221 | 0xDD   | Highest Fire resistance       |
| 222 | 0xDE   | Highest Ice resistance        |
| 223 | 0xDF   | Highest Thunder resistance    |
| 224 | 0xE0   | Highest Earth resistance      |
| 225 | 0xE1   | Highest Poison resistance     |
| 226 | 0xE2   | Highest Wind resistance       |
| 227 | 0xE3   | Highest Water resistance      |
| 228 | 0xE4   | Highest Holy resistance       |
| 229 | 0xE5   | Lowest Fire resistance        |
| 230 | 0xE6   | Lowest Ice resistance         |
| 231 | 0xE7   | Lowest Thunder resistance     |
| 232 | 0xE8   | Lowest Earth resistance       |
| 233 | 0xE9   | Lowest Poison resistance      |
| 234 | 0xEA   | Lowest Wind resistance        |
| 235 | 0xEB   | Lowest Water resistance       |
| 236 | 0xEC   | Lowest Holy resistance        |



