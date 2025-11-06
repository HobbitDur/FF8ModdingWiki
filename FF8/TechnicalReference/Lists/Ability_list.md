---
layout: default
title: Ability List
parent: List
permalink: /technical-reference/list/ability-list/
---

# Ability list

## Abilities Type

This ID define which list should be check. Seifer is a special case for seifer but point to same list than custom.

| ID  | Name                                                                                 |
|-----|--------------------------------------------------------------------------------------|
| 0   | Not defined                                                                          |
| 2   | [Magic]({{site.baseurl}}/FF8/TechnicalReference/Lists/Magic_list)                    |
| 4   | [Item]({{site.baseurl}}/FF8/TechnicalReference/Lists/Item_list)                      |
| 8   | [Custom]({{site.baseurl}}/FF8/TechnicalReference/Lists/Ability_list#monster-ability) |
| 179 | Ultimecia_weird_file_127                                                             |
| 236 | [Seifer]({{site.baseurl}}/FF8/TechnicalReference/Lists/Ability_list#monster-ability) |

## Passif abilities

| Bit Position | Flag (Hex) | Description    |
|--------------|------------|----------------|
| 0            | 0x1        | Alert          |
| 1            | 0x2        | Rare Item      |
| 2            | 0x4        | Encounter Half |
| 3            | 0x8        | Encounter None |
| 4            | 0x10       | Move Find      |

# Monster ability

| id  | hex   | name                                  |
|-----|-------|---------------------------------------|
| 0   | 0x00  | Not defined                           |
| 1   | 0x01  | Unnamed                               |
| 2   | 0x02  | Physical attack                       |
| 3   | 0x03  | Attack (Cronos)                       |
| 4   | 0x04  | Attack (Ultimecia)                    |
| 5   | 0x05  | Blade Slice                           |
| 6   | 0x06  | Hind Kick                             |
| 7   | 0x07  | Blade Shot                            |
| 8   | 0x08  | Ray Bomb                              |
| 9   | 0x09  | Storm Breath                          |
| 10  | 0x0A  | Dark Mist                             |
| 11  | 0x0B  | Squeeze                               |
| 12  | 0x0C  | Clash                                 |
| 13  | 0x0D  | Arm Crush                             |
| 14  | 0x0E  | Unused X-ATM092 Attack?               |
| 15  | 0x0F  | Tail Needle                           |
| 16  | 0x10  | Arm Slash                             |
| 17  | 0x11  | Bad Breath                            |
| 18  | 0x12  | Geezard Bites                         |
| 19  | 0x13  | Petrify Stare                         |
| 20  | 0x14  | Vampire                               |
| 21  | 0x15  | Poison Mist                           |
| 22  | 0x16  | Counter Slice                         |
| 23  | 0x17  | Counter Laser Eye                     |
| 24  | 0x18  | Unnamed                               |
| 25  | 0x19  | 1000 Needles                          |
| 26  | 0x1A  | Heartbreak                            |
| 27  | 0x1B  | Upward Kick                           |
| 28  | 0x1C  | Electric Discharge                    |
| 29  | 0x1D  | Petrify Stare                         |
| 30  | 0x1E  | Low-Petrify Stare ?Gallus sub-fossile |
| 31  | 0x1F  | Bite                                  |
| 32  | 0x20  | Poison Gas                            |
| 33  | 0x21  | Poison Gas                            |
| 34  | 0x22  | Poison Gas                            |
| 35  | 0x23  | Acid                                  |
| 36  | 0x24  | Melt-Eye                              |
| 37  | 0x25  | Breath                                |
| 38  | 0x26  | Ice Breath                            |
| 39  | 0x27  | Sand Storm                            |
| 40  | 0x28  | Unnamed                               |
| 41  | 0x29  | Unnamed                               |
| 42  | 0x2A  | Attack (Diodon)                       |
| 43  | 0x2B  | Attack (Phantom)                      |
| 44  | 0x2C  | Unnamed                               |
| 45  | 0x2D  | Wedge Enter Battle                    |
| 46  | 0x2E  | Attack medium (Satyrux)               |
| 47  | 0x2F  | Attack strong (Satyrux)               |
| 48  | 0x30  | Draw                                  |
| 49  | 0x31  | Earthquake                            |
| 50  | 0x32  | Attack (Scavenger)                    |
| 51  | 0x33  | Unnamed                               |
| 52  | 0x34  | Unnamed                               |
| 53  | 0x35  | Morph                                 |
| 54  | 0x36  | Arm Hug                               |
| 55  | 0x37  | Power Bomb                            |
| 56  | 0x38  | Dribble                               |
| 57  | 0x39  | Shoot                                 |
| 58  | 0x3A  | Ultrasonic Waves                      |
| 59  | 0x3B  | Ifrit Strong Punch                    |
| 60  | 0x3C  | BiteBite                              |
| 61  | 0x3D  | Shotgun                               |
| 62  | 0x3E  | Suicide                               |
| 63  | 0x3F  | Ultrasonic Waves                      |
| 64  | 0x40  | Breath of Death                       |
| 65  | 0x41  | Disease Breath                        |
| 66  | 0x42  | Sticky Icky                           |
| 67  | 0x43  | Shoulder Charge                       |
| 68  | 0x44  | Gatling Gun                           |
| 69  | 0x45  | Cannon Blow                           |
| 70  | 0x46  | Wild Cannon Blow                      |
| 71  | 0x47  | Store                                 |
| 72  | 0x48  | Degenerator                           |
| 73  | 0x49  | Telekinesis                           |
| 74  | 0x4A  | Do Nothing?                           |
| 75  | 0x4B  | Attack (Aphide)                       |
| 76  | 0x4C  | Hypnotize                             |
| 77  | 0x4D  | Gastric Juice                         |
| 78  | 0x4E  | Attack (Ao)                           |
| 79  | 0x4F  | Ifrit Weak Punch                      |
| 80  | 0x50  | Sand Storm                            |
| 81  | 0x51  | Attack (Fatima)                       |
| 82  | 0x52  | Unnamed                               |
| 83  | 0x53  | Unnamed                               |
| 84  | 0x54  | Stare                                 |
| 85  | 0x55  | Sigh                                  |
| 86  | 0x56  | Curse                                 |
| 87  | 0x57  | Attack (Cariatide)                    |
| 88  | 0x58  | Ifrit HP < 50%                        |
| 89  | 0x59  | Ifrit Shiva Summoned 1st time         |
| 90  | 0x5A  | Ifrit Death                           |
| 91  | 0x5B  | Ifrit Defeated by Shiva               |
| 92  | 0x5C  | Attack (Moloch)                       |
| 93  | 0x5D  | Grab Punch                            |
| 94  | 0x5E  | Breath                                |
| 95  | 0x5F  | Double Sword                          |
| 96  | 0x60  | Thrust                                |
| 97  | 0x61  | Iai Blow                              |
| 98  | 0x62  | Ultra Waves                           |
| 99  | 0x63  | Caterchipillar Bite                   |
| 100 | 0x64  | Sticky Web                            |
| 101 | 0x65  | Attack (Feng)                         |
| 102 | 0x66  | Breath                                |
| 103 | 0x67  | Tail Blade                            |
| 104 | 0x68  | Unnamed                               |
| 105 | 0x69  | Unnamed                               |
| 106 | 0x6A  | Mega Spark                            |
| 107 | 0x6B  | Onrush                                |
| 108 | 0x6C  | T-Rexaur Tail Attack                  |
| 109 | 0x6D  | T-Rexaur Magic Counter                |
| 110 | 0x6E  | Fart                                  |
| 111 | 0x6F  | Needle                                |
| 112 | 0x70  | Gastric Juice                         |
| 113 | 0x71  | Sleeping Gas                          |
| 114 | 0x72  | Breath                                |
| 115 | 0x73  | Attack (Fungus)                       |
| 116 | 0x74  | Unmissable attack (Biggs 2)           |
| 117 | 0x75  | Attack (BGH251F2)                     |
| 118 | 0x76  | Beam Cannon                           |
| 119 | 0x77  | BGH251F2 second fight destruction     |
| 120 | 0x78  | Magma Breath                          |
| 121 | 0x79  | Resonance                             |
| 122 | 0x7A  | Blaster                               |
| 123 | 0x7B  | Blaster                               |
| 124 | 0x7C  | LV5 Death                             |
| 125 | 0x7D  | Death Claw                            |
| 126 | 0x7E  | Bear Hug                              |
| 127 | 0x7F  | Gas                                   |
| 128 | 0x80  | Explosion                             |
| 129 | 0x81  | Explosion                             |
| 130 | 0x82  | Explosion                             |
| 131 | 0x83  | ",Brrawghh!,"                         |
| 132 | 0x84  | Unnamed                               |
| 133 | 0x85  | Wind Blast                            |
| 134 | 0x86  | Attack (Thrustaevis)                  |
| 135 | 0x87  | Scan                                  |
| 136 | 0x88  | Cerberus Counter 1                    |
| 137 | 0x89  | Cerberus Counter 2                    |
| 138 | 0x8A  | BGH251F2 Gatling Gun                  |
| 139 | 0x8B  | Beam Cannon                           |
| 140 | 0x8C  | BGH251F2 1st Turret Exploding         |
| 141 | 0x8D  | BGH251F2 2nd Turret Exploding         |
| 142 | 0x8E  | BGH251F2 3rd Turret Exploding         |
| 143 | 0x8F  | BGH251F2 4th Turret Exploding         |
| 144 | 0x90  | BGH251F2 Death                        |
| 145 | 0x91  | X-ATM092 Death                        |
| 146 | 0x92  | Aqua Breath                           |
| 147 | 0x93  | BGH251F2 1st Turret Exploding         |
| 148 | 0x94  | BGH251F2 2nd Turret Exploding         |
| 149 | 0x95  | BGH251F2 3rd Turret Exploding         |
| 150 | 0x96  | BGH251F2 4th Turret Exploding         |
| 151 | 0x97  | Fake President Death                  |
| 152 | 0x98  | Evil-Eye                              |
| 153 | 0x99  | Counter Twist                         |
| 154 | 0x9A  | Chaingun                              |
| 155 | 0x9B  | Snipe Laser                           |
| 156 | 0x9C  | Unmissable attack                     |
| 157 | 0x9D  | Melting Bubble                        |
| 158 | 0x9E  | Super Arm                             |
| 159 | 0x9F  | Boomerang Sword                       |
| 160 | 0xA0  | Unnamed                               |
| 161 | 0xA1  | Base Leader Message 1                 |
| 162 | 0xA2  | Base Leader Message 2                 |
| 163 | 0xA3  | Base Leader Message 3                 |
| 164 | 0xA4  | Base Leader Message 4                 |
| 165 | 0xA5  | Punch (Esthar Soldier)                |
| 166 | 0xA6  | Grand Sword                           |
| 167 | 0xA7  | Attack (Attila, Ekarissor)            |
| 168 | 0xA8  | Psycho Blast                          |
| 169 | 0xA9  | Sticky Web                            |
| 170 | 0xAA  | Unnamed                               |
| 171 | 0xAB  | Unnamed                               |
| 172 | 0xAC  | Unnamed                               |
| 173 | 0xAD  | Unnamed                               |
| 174 | 0xAE  | Sand Shake                            |
| 175 | 0xAF  | Saliva                                |
| 176 | 0xB0  | Beam Laser                            |
| 177 | 0xB1  | Reflect Beam                          |
| 178 | 0xB2  | Unnamed                               |
| 179 | 0xB3  | Unnamed                               |
| 180 | 0xB4  | Oil Shot                              |
| 181 | 0xB5  | Oil Blast                             |
| 182 | 0xB6  | Sonic Wave                            |
| 183 | 0xB7  | Dissolving Acid                       |
| 184 | 0xB8  | Bad Breath                            |
| 185 | 0xB9  | Eerie Sound Wave                      |
| 186 | 0xBA  | Unnamed                               |
| 187 | 0xBB  | Unnamed                               |
| 188 | 0xBC  | Unnamed                               |
| 189 | 0xBD  | Plague attack (Hornet)                |
| 190 | 0xBE  | Attack (Hornet)                       |
| 191 | 0xBF  | Unnamed                               |
| 192 | 0xC0  | Ochu Dance                            |
| 193 | 0xC1  | Earthquake                            |
| 194 | 0xC2  | Drink Magic                           |
| 195 | 0xC3  | Poison attack (Trogiidae)             |
| 196 | 0xC4  | Unnamed                               |
| 197 | 0xC5  | Unnamed                               |
| 198 | 0xC6  | Unnamed                               |
| 199 | 0xC7  | Assault Horn                          |
| 200 | 0xC8  | Ray Bomb                              |
| 201 | 0xC9  | Micro Missiles                        |
| 202 | 0xCA  | Strong attack (Attila)                |
| 203 | 0xCB  | Unnamed                               |
| 204 | 0xCC  | Astral Punch                          |
| 205 | 0xCD  | Unnamed                               |
| 206 | 0xCE  | Unnamed                               |
| 207 | 0xCF  | Unnamed                               |
| 208 | 0xD0  | Unnamed                               |
| 209 | 0xD1  | Unnamed                               |
| 210 | 0xD2  | Raijin Special                        |
| 211 | 0xD3  | Minotaur Earth Regen                  |
| 212 | 0xD4  | Sacred Earth Regen                    |
| 213 | 0xD5  | Mad Cow Special                       |
| 214 | 0xD6  | Zan                                   |
| 215 | 0xD7  | Metsu                                 |
| 216 | 0xD8  | Sai                                   |
| 217 | 0xD9  | Unnamed                               |
| 218 | 0xDA  | Unnamed                               |
| 219 | 0xDB  | Unnamed                               |
| 220 | 0xDC  | Mower                                 |
| 221 | 0xDD  | Unnamed                               |
| 222 | 0xDE  | Chef's Knife                          |
| 223 | 0xDF  | Everyone's Grudge                     |
| 224 | 0xE0  | Unnamed                               |
| 225 | 0xE1  | Tonberry King Death                   |
| 226 | 0xE2  | Junk                                  |
| 227 | 0xE3  | It's sharp!                           |
| 228 | 0xE4  | Unnamed                               |
| 229 | 0xE5  | Unnamed                               |
| 230 | 0xE6  | 10.000 Needles                        |
| 231 | 0xE7  | Ker Plunk                             |
| 232 | 0xE8  | Unnamed                               |
| 233 | 0xE9  | Storm Breath                          |
| 234 | 0xEA  | Mega Flare                            |
| 235 | 0xEB  | Barrier Change                        |
| 236 | 0xEC  | Minotaur Death v1                     |
| 237 | 0xED  | Minotaur Death v2                     |
| 238 | 0xEE  | Sacred Death (1st Battle)             |
| 239 | 0xEF  | Sacred Death v1 (2nd battle)          |
| 240 | 0xF0  | Sacred Death v2 (2nd battle)          |
| 241 | 0xF1  | Unnamed                               |
| 242 | 0xF2  | Thunder Summon                        |
| 243 | 0xF3  | Deadly Horn                           |
| 244 | 0xF4  | Raldo Ball                            |
| 245 | 0xF5  | Raldo Ball                            |
| 246 | 0xF6  | Raldo Ball                            |
| 247 | 0xF7  | Raldo Throw                           |
| 248 | 0xF8  | Raldo Throw                           |
| 249 | 0xF9  | Raldo Throw                           |
| 250 | 0xFA  | Bahamut Dialog                        |
| 251 | 0xFB  | Bahamut Dialog                        |
| 252 | 0xFC  | Bahamut Dialog                        |
| 253 | 0xFD  | Bahamut Dialog                        |
| 254 | 0xFE  | Bahamut Dialog                        |
| 255 | 0xFF  | Bahamut Dialog                        |
| 256 | 0x100 | Bahamut Death                         |
| 257 | 0x101 | Gravija                               |
| 258 | 0x102 | Remove mask (Brahman)                 |
| 259 | 0x103 | Unnamed                               |
| 260 | 0x104 | Unnamed                               |
| 261 | 0x105 | Magic Summon                          |
| 262 | 0x106 | Mighty Guard                          |
| 263 | 0x107 | Doom                                  |
| 264 | 0x108 | Unnamed                               |
| 265 | 0x109 | Unnamed                               |
| 266 | 0x10A | Unnamed                               |
| 267 | 0x10B | Unnamed                               |
| 268 | 0x10C | Unnamed                               |
| 269 | 0x10D | Unnamed                               |
| 270 | 0x10E | Thunder attack (Tikal)                |
| 271 | 0x10F | Thunder                               |
| 272 | 0x110 | Thundara                              |
| 273 | 0x111 | Thundaga                              |
| 274 | 0x112 | Zantetsuken                           |
| 275 | 0x113 | Unnamed                               |
| 276 | 0x114 | White Wind                            |
| 277 | 0x115 | Unnamed                               |
| 278 | 0x116 | Strong counter-attack (Krystal)       |
| 279 | 0x117 | Counter-attack (Krystal)              |
| 280 | 0x118 | Charge                                |
| 281 | 0x119 | Homing Laser                          |
| 282 | 0x11A | Homing Laser                          |
| 283 | 0x11B | Twin Homing Laser                     |
| 284 | 0x11C | Corona                                |
| 285 | 0x11D | Megiddo Flame                         |
| 286 | 0x11E | Unnamed                               |
| 287 | 0x11F | NORG Pod Opening                      |
| 288 | 0x120 | NORG Tutorial?                        |
| 289 | 0x121 | NORG Death                            |
| 290 | 0x122 | Unnamed                               |
| 291 | 0x123 | Unnamed                               |
| 292 | 0x124 | Mega Pulse Cannon                     |
| 293 | 0x125 | Mini Pulse Cannon                     |
| 294 | 0x126 | Unmissable attack (Raijin 3)          |
| 295 | 0x127 | Mighty Guard                          |
| 296 | 0x128 | Unnamed                               |
| 297 | 0x129 | Unnamed                               |
| 298 | 0x12A | Unnamed                               |
| 299 | 0x12B | Unnamed                               |
| 300 | 0x12C | Unnamed                               |
| 301 | 0x12D | Unnamed                               |
| 302 | 0x12E | Unnamed                               |
| 303 | 0x12F | Unnamed                               |
| 304 | 0x130 | Unnamed                               |
| 305 | 0x131 | Dark Flare                            |
| 306 | 0x132 | Unnamed                               |
| 307 | 0x133 | Soul Crush                            |
| 308 | 0x134 | Light Pillar                          |
| 309 | 0x135 | Gravija                               |
| 310 | 0x136 | Megiddo Flame                         |
| 311 | 0x137 | Terra Break                           |
| 312 | 0x138 | Ultima Weapon Death                   |
| 313 | 0x139 | Unnamed                               |
| 314 | 0x13A | Demon Slice                           |
| 315 | 0x13B | Bloodfest                             |
| 316 | 0x13C | Engery Bomber                         |
| 317 | 0x13D | Adel Death                            |
| 318 | 0x13E | Adel's Drain                          |
| 319 | 0x13F | "Sorceress" Spawn                     |
| 320 | 0x140 | Unnamed                               |
| 321 | 0x141 | Unnamed                               |
| 322 | 0x142 | Unnamed                               |
| 323 | 0x143 | Unnamed                               |
| 324 | 0x144 | Unnamed                               |
| 325 | 0x145 | Unnamed                               |
| 326 | 0x146 | Unnamed                               |
| 327 | 0x147 | "Sorceress" Spawn                     |
| 328 | 0x148 | Final "Sorceress" Death               |
| 329 | 0x149 | Zantetsuken                           |
| 330 | 0x14A | Gilgamesh kill Seifer                 |
| 331 | 0x14B | Unnamed                               |
| 332 | 0x14C | Unnamed                               |
| 333 | 0x14D | Unnamed                               |
| 334 | 0x14E | Unnamed                               |
| 335 | 0x14F | G-Force ejection (Cronos/Ultimecia)   |
| 336 | 0x150 | Absorbed into time...                 |
| 337 | 0x151 | Ultimecia Blow Away Magic             |
| 338 | 0x152 | Maelstrom                             |
| 339 | 0x153 | Ultimecia First Death                 |
| 340 | 0x154 | Seifer counter Zantetsuken            |
| 341 | 0x155 | Seifer death without Gilgamesh        |
| 342 | 0x156 | Unnamed                               |
| 343 | 0x157 | Unnamed                               |
| 344 | 0x158 | Unnamed                               |
| 345 | 0x159 | Unnamed                               |
| 346 | 0x15A | Unnamed                               |
| 347 | 0x15B | Unnamed                               |
| 348 | 0x15C | Unnamed                               |
| 349 | 0x15D | Unnamed                               |
| 350 | 0x15E | Griever Summon                        |
| 351 | 0x15F | Griever Death                         |
| 352 | 0x160 | Ultimecia Junctioning to Griever      |
| 353 | 0x161 | Griever Tail Falling Off              |
| 354 | 0x162 | Griever + Ultimecia Death             |
| 355 | 0x163 | Ultimecia Final Form Spawn            |
| 356 | 0x164 | Ultimecia Final Form Death            |
| 357 | 0x165 | Draw Apocalypse                       |
| 358 | 0x166 | Hell's Judgement                      |
| 359 | 0x167 | Drain                                 |
| 360 | 0x168 | Great Attractor                       |
| 361 | 0x169 | Unmissable attack (Helix)             |
| 362 | 0x16A | Shockwave Pulsar                      |
| 363 | 0x16B | Unnamed                               |
| 364 | 0x16C | Esuna                                 |
| 365 | 0x16D | Maelstrom                             |
| 366 | 0x16E | Unmissable attack (Necro 1)           |
| 367 | 0x16F | Unmissable attack (Necro 2)           |
| 368 | 0x170 | Unnamed                               |
| 369 | 0x171 | Vacuum Wave                           |
| 370 | 0x172 | Unnamed                               |
| 371 | 0x173 | Unnamed                               |
| 372 | 0x174 | Unnamed                               |
| 373 | 0x175 | Apocalypse                            |
| 374 | 0x176 | Unnamed                               |
| 375 | 0x177 | Gigantic Sword                        |
| 376 | 0x178 | Unnamed                               |
| 377 | 0x179 | Seifer Physical Attack                |
| 378 | 0x17A | Ultima                                |
| 379 | 0x17B | Holy                                  |
| 380 | 0x17C | Quake                                 |
| 381 | 0x17D | Tornado                               |
| 382 | 0x17E | Unnamed                               |
| 383 | 0x17F | Unnamed                               |

# Chara abilities

| Bit Position | Ability       |
|--------------|---------------|
| 1            | Mug           |
| 2            | Med Data      |
| 3            | Counter       |
| 4            | Return Damage |
| 5            | Cover         |
| 6            | Initiative    |
| 7            | Move-HP Up    |
| 8            | HP Bonus      |
| 9            | Str Bonus     |
| 10           | Vit Bonus     |
| 11           | Mag Bonus     |
| 12           | Spr Bonus     |
| 13           | Auto-Protect  |
| 14           | Auto-Shell    |
| 15           | Auto-Reflect  |
| 16           | Auto-Haste    |
| 17           | Auto-Potion   |
| 18           | Expendx2-1    |
| 19           | Expendx3-1    |
| 20           | Ribbon        |