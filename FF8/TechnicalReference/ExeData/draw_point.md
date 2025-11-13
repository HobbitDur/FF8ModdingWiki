---
layout: default
title: Draw point
parent: ExeData
author: HobbitDur
permalink: /technical-reference/exedata/draw-point/
---

1. TOC
{:toc}


# Field Draw Notes

## General info
All information for a Draw Point is stored in a single byte; the spell ID, whether the draw point refreshes,
and whether you get a low or high yield from the draw point.

Start with the spell ID, and then modify it if necessary:
Add 64 to Decimal ID for 2nd Bit - Refill Behavior (Added = Yes, Not Added = No)
Add 128 to Decimal ID for 1st Bit - Draw Yield (Added = High, Not Added = Low)
Add 192 to Decimal ID for Refill + High Yield to both be applied.

Each value corresponds to a 'Draw ID' that is referenced in the field script. For example, the field script for a draw point
is quite basic and will just read 'drawpoint(15)' for instance.

## Default values
Address Starts:
0x00B92328

Default Values
.data:00B92328 byte_B92328     db 55h, 44h, 99h, 9Bh, 0Dh, 0CCh, 0C7h, 0D5h, 0C1h, 0E9h  
.data:00B92500                 db 0E6h, 72h, 55h, 6, 0E3h, 0D8h, 0DEh, 0DDh, 21h, 0A0h  
.data:00B92500                 db 55h, 4Ah, 48h, 70h, 5Bh, 4Ch, 0C2h, 0EEh, 9, 4Bh, 0C5h  
.data:00B92500                 db 0E6h, 59h, 0ECh, 0DCh, 17h, 1Fh, 0DDh, 0EFh, 56h, 0E3h  
.data:00B92500                 db 0DEh, 0DAh, 19h, 93h, 0C9h, 10h, 57h, 44h, 0D1h, 52h  
.data:00B92500                 db 0E1h, 2Dh, 0Fh, 65h, 65h, 0D8h, 1Fh, 0EBh, 0Eh, 69h  
.data:00B92500                 db 13h, 67h, 6Ah, 0D0h, 57h, 64h, 57h, 0Fh, 8Eh, 68h, 0E7h  
.data:00B92500                 db 4Bh, 2Ch, 2Dh, 0C9h, 30h, 20h, 0D3h, 46h, 43h, 0D2h  
.data:00B92500                 db 0CEh, 56h, 58h, 19h, 5Ch, 5Bh, 0A2h, 13h, 0F1h, 10h  
.data:00B92500                 db 0E3h, 0E4h, 0D7h, 0D8h, 0E5h, 0DAh, 0E1h, 22h, 0Fh  
.data:00B92500                 db 57h, 56h, 72h, 5Bh, 64h, 5Ch, 65h, 58h, 0Fh, 20h, 0Eh  
.data:00B92500                 db 10h, 31h, 13h, 19h, 22h, 81h, 81h, 81h, 81h, 81h, 81h  
.data:00B92500                 db 81h, 81h, 81h, 81h, 81h, 55h, 5Bh, 47h, 42h, 48h, 45h  
.data:00B92500                 db 44h, 41h, 55h, 4Ah, 56h, 5Bh, 72h, 5Eh, 63h, 4Bh, 4Ch  
.data:00B92500                 db 58h, 4Dh, 5Dh, 4Eh, 49h, 65h, 43h, 5Ah, 46h, 67h, 4Fh  
.data:00B92500                 db 5Ch, 64h, 51h, 57h, 52h, 19h, 5Fh, 20h, 11h, 61h, 6Ah  
.data:00B92500                 db 10h, 13h, 22h, 67h, 66h, 0D1h, 68h, 69h, 0CFh, 6Bh  
.data:00B92500                 db 6Ch, 0EDh, 6Eh, 6Fh, 70h, 71h, 93h, 0D2h, 0D1h, 0D0h  
.data:00B92500                 db 0CEh, 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D2h, 0D1h, 0D0h  
.data:00B92500                 db 0CEh, 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D2h, 0D1h, 0D0h  
.data:00B92500                 db 0CEh, 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D3h, 0D0h, 0CEh  
.data:00B92500                 db 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D0h, 0CEh, 0E2h, 0E0h  
.data:00B92500                 db 0D3h, 0E2h, 0D9h, 0D0h, 0CEh, 0CFh, 0E0h, 0D3h, 0E2h  
.data:00B92500                 db 0D9h, 0D0h, 0E2h, 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D0h  
.data:00B92500                 db 0CEh, 0CFh, 0E0h, 0D3h, 44h, 55h, 0DCh, 0E7h, 10h, 21h  
.data:00B92500                 db 20h, 0Eh, 0Fh, 13h, 0F2h  

## Explanation
255 Draw Points, that the Field Script can reference. Each value is a spell ID, whether the draw point refills,
and whether the draw point gives a low or high yield.


Example:
You want to edit Draw ID 15
- 15 -1 = 14 (want to start counting from 0 instead of 1)
- 792500 + 14 = 79250E (location of Draw ID 15)

If you want to set it to give Cure, which is MagicID #15 in the bin,
then you input the following value:
- 0x15 (Cure, no refill)
- 0x55 (Cure, refills)

Represented in binary, it'd look like this:
- 0x15 = 00010101 (Cure, no refill)
- 0x55 = 01010101 (Cure, refills)

The 01 at the start of 0x55 is two bits that set a bool for refill.
Keep an eye out for that when setting the value (I think I added this note for debugging or something)

Visiblity seems to be set from Field in group's Init.
0 for hidden, 1 for visible.

From the Wiki (some additional info on how it works, like refill):

| State ID | 	Description                           |
|----------|----------------------------------------|
| 0        | 	Fully stocked                         |
| 1        | 	Partially stocked                     |
| 2        | 	Empty but refills (white swirl)       |
| 3        | 	Empty and doesn't refill (blue swirl) |

Draw points start off at state 0 and move to state 2 or 3 when drawn from.
There are two flags for each draw point, one which defines if the draw point is rich, and one which defines if it refills.


## Draw Points

magic_id = byte & 0x3F
refill = (byte >> 6) & 1 (0x40)
extra_magic = byte >> 7 (0x80)

Walk-Restock Check: 
- Every 10,240 steps it checks it
- Var 164 (savegame + 0xE14)

Each Draw is then given a random number 0 - 32,767
- ended with 1 (x86 TEST opcode) for a 50% chance
- that it'll be restocked.

Unknown16 in Field script binds Drawpoint to Variable
- Is usually the same as Draw ID.
- Stored at Field Vars 100-164 (Savegame + 0xDD4)
	

1st Bit determines the amount you can draw, calculated as:
- 6-15 if fully stocked with bit set
- 3-8 if partial, bit set/fully if bit not set
- 2-4 if partial, no bit set

World Map is: 2-5 with bit-set, 1-2 if not set  
So in practice, if its = 0 you get 3-8 or 2-4.  
			if its = 1 you get 6-15 or 3-8  

## List default draw point
001 0 1 Cure - Balamb Garden courtyard  
002 0 1 Blizzard - Balamb Garden training center  
003 1 0 Full-Life - Balamb Garden MD level  
004 1 0 Esuna - Balamb Garden library next to the book shelf  
005 0 0 Demi - Balamb Garden cafeteria (only during Garden Riot)  
006 1 1 Bio - Balamb Garden B2 floor  
007 1 1 Thunder - Balamb outside junk shop  
008 1 1 Cure - Balamb harbor  
009 1 1 Fire - Fire Cavern  
010 1 1 Silence - Dollet town square  
011 1 1 Blind - Dollet Communications Tower  
012 0 1 Scan - Timber Pub Aurora back alley  
013 0 1 Cure - Timber outside the pub  
014 0 0 Blizzaga - Timber Maniacs Building left room  
015 1 1 Haste - Galbadia Garden lobby  
016 1 1 Life - Galbadia Garden changing rooms  
017 1 1 Shell - Galbadia Garden courtyard  
018 1 1 Protect - Galbadia Garden ice rink  
019 0 0 Double - Galbadia Garden auditorium  
020 1 0 Aura - Outside Galbadia Garden during Garden war  
021 0 1 Cure - Timber forests in a Laguna dream  
022 0 1 Water - Timber forests in a Laguna dream  
023 0 1 Thundara - Deling City park  
024 0 1 Zombie - Deling City Sewers  
025 0 1 Esuna - Deling City Sewers  
026 0 1 Bio - Deling City Sewers  
027 1 1 Fira  
028 1 1 Berserk - D-District Prison Floor 9 - right cell  
029 0 0 Thundaga - D-District Prison Floor 11 - right cell  
030 0 1 Aero - Outside D-District Prison  
031 1 1 Blizzara - Missile Base - control room  
032 1 1 Blind - Missile Base room with G-Soldiers who ask to deliver a message  
033 0 1 Full-Life - Missile Base - silo room  
034 1 1 Drain - Winhill road south from town square  
035 1 1 Dispel - Winhill town square  
036 0 0 Curaga - Winhill Laguna's room in the dream  
037 0 0 Reflect - Winhill east road  
038 1 1 Protect - Tomb of the Unknown King - outside  
039 1 1 Float - Tomb of the Unknown King - north room  
040 0 1 Cura - Tomb of the Unknown King - east room  
041 1 1 Haste - Fishermans Horizon abandoned train station  
042 1 1 Shell - Fishermans Horizon junk shop  
043 1 1 Regen - Fishermans Horizon overlooking the sun panel  
044 0 0 Full-Life - Fishermans Horizon Master Fisherman's fishing spot  
045 1 0 Ultima - Fishermans Horizon mayor's house  
046 1 1 Thundaga - Great Salt Lake past the dinosaur skeleton  
047 0 0 Meteor - Great Salt Lake dinosaur skeleton  
048 0 1 Curaga - Esthar city streets near city entrance  
049 0 1 Blizzard - Esthar outside palace  
050 1 1 Quake - Esthar outside Odine's Lab  
051 0 1 Tornado - Esthar shopping mall  
052 1 1 Double - Esthar Odine's Lab in a Laguna dream  
053 0 0 Pain  
054 0 0 Flare - Esthar Odine's Lab in a Laguna dream  
055 0 1 Stop - Sorceress Memorial  
056 0 1 Stop  
057 1 1 Life - Tears' Point entrance  
058 0 0 Reflect - Tears' Point middle  
059 1 1 Death - Lunatic Pandora Laboratory in a Laguna dream  
060 0 0 Holy - Lunatic Pandora near Elevator #1  
061 0 1 Silence - Lunatic Pandora  
062 0 0 Ultima - Lunatic Pandora  
063 0 1 Confuse  
064 0 1 Break - Lunatic Pandora on the way to fight Adel  
065 1 1 Meteor - Lunatic Pandora entrance  
066 0 1 Curaga - Lunatic Pandora elevator room  
067 0 1 Slow  
068 0 1 Curaga - Edea's Orphanage  
069 0 0 Flare  
070 1 0 Holy  
071 0 1 Sleep - Centra Excavation Site  
072 1 1 Confuse - Centra Excavation Site  
073 0 1 Aero - Centra Ruins right ladder after the lift  
074 0 0 Drain - Centra Ruins platform after the first staircase  
075 0 0 Pain - Centra Ruins next to the dome  
076 1 1 Thundaga - Trabia Garden in front of the statue  
077 0 0 Zombie - Trabia Garden cemetery  
078 0 0 Aura - Trabia Garden stage  
079 1 1 Ultima - Shumi Village - above ground  
080 0 1 Blizzaga - Shumi Village - outside elder's house  
081 0 1 Firaga - Shumi Village workshop  
082 1 1 Tornado  
083 1 1 Holy - White SeeD Ship  
084 0 1 Cura - Ragnarok room with a red Propagator  
085 0 1 Life - Ragnarok hangar upstairs  
086 0 0 Full-Life - Ragnarok room with save point  
087 0 1 Dispel - Deep Sea Research Center second level  
088 0 1 Esuna - Deep Sea Research Center secret room  
089 1 0 Triple - Deep Sea Research Center third screen on the way to Ultima Weapon's lair  
090 0 0 Ultima - Deep Sea Research Center fifth screen on the way to Ultima Weapon's lair  
091 1 1 Meltdown - Lunar Base room before the escape pods  
092 0 0 Meteor - Lunar Base Ellone's room  
093 1 1 Haste  
094 1 1 Slow  
095 1 1 Curaga  
096 1 1 Life  
097 1 1 Stop  
098 1 1 Regen  
099 1 1 Double  
100 0 0 Triple  
101 0 0 Flare - Ultimecia Castle outside  
102 0 1 Curaga - Ultimecia Castle storage room  
103 0 1 Cura - Ultimecia Castle passageway  
104 0 1 Scan  
105 0 1 Esuna  
106 0 1 Slow - Ultimecia Castle courtyard  
107 0 1 Dispel - Ultimecia Castle chapel  
108 0 1 Stop - Ultimecia Castle clock tower  
109 0 1 Life  
110 0 0 Flare  
111 0 0 Aura - Ultimecia Castle wine cellar  
112 0 0 Holy - Ultimecia Castle treasure room  
113 0 0 Meteor  
114 0 0 Meltdown - Ultimecia Castle art gallery  
115 0 0 Ultima - Ultimecia Castle armory  
116 0 0 Full-Life - Ultimecia Castle prison  
117 0 0 Triple  
118 1 0 Fire  
119 1 0 Fire  
120 1 0 Fire  
121 1 0 Fire  
122 1 0 Fire  
123 1 0 Fire  
124 1 0 Fire  
125 1 0 Fire  
126 1 0 Fire  
127 1 0 Fire  
128 1 0 Fire  
129 0 1 Cure  
130 0 1 Esuna  
131 0 1 Thunder  
132 0 1 Fira  
133 0 1 Thundara  
134 0 1 Blizzara  
135 0 1 Blizzard  
136 0 1 Fire  
137 0 1 Cure  
138 0 1 Water  
139 0 1 Cura  
140 0 1 Esuna  
141 0 1 Scan  
142 0 1 Shell  
143 0 1 Haste  
144 0 1 Aero  
145 0 1 Bio  
146 0 1 Life  
147 0 1 Demi  
148 0 1 Protect  
149 0 1 Holy  
150 0 1 Thundaga  
151 0 1 Stop  
152 0 1 Firaga  
153 0 1 Regen  
154 0 1 Blizzaga  
155 0 1 Confuse  
156 0 1 Flare  
157 0 1 Dispel  
158 0 1 Slow  
159 0 1 Quake  
160 0 1 Curaga  
161 0 1 Tornado  
162 0 0 Full-Life  
163 0 1 Reflect  
164 0 0 Aura  
165 0 0 Quake  
166 0 1 Double  
167 0 1 Break  
168 0 0 Meteor  
169 0 0 Ultima  
170 0 0 Triple  
171 0 1 Confuse  
172 0 1 Blind  
173 1 1 Quake  
174 0 1 Sleep  
175 0 1 Silence  
176 1 1 Flare  
177 0 1 Death  
178 0 1 Drain  
179 1 1 Pain  
180 0 1 Berserk  
181 0 1 Float  
182 0 1 Zombie  
183 0 1 Meltdown  
184 1 0 Ultima  
185 1 1 Tornado  
186 1 1 Quake  
187 1 1 Meteor  
188 1 1 Holy  
189 1 1 Flare  
190 1 1 Aura  
191 1 1 Ultima  
192 1 1 Triple  
193 1 1 Full-Life  
194 1 1 Tornado  
195 1 1 Quake  
196 1 1 Meteor  
197 1 1 Holy  
198 1 1 Flare  
199 1 1 Aura  
200 1 1 Ultima  
201 1 1 Triple  
202 1 1 Full-Life  
203 1 1 Tornado  
204 1 1 Quake  
205 1 1 Meteor  
206 1 1 Holy  
207 1 1 Flare  
208 1 1 Aura  
209 1 1 Ultima  
210 1 1 Triple  
211 1 1 Full-Life  
212 1 1 Ultima  
213 1 1 Meteor  
214 1 1 Holy  
215 1 1 Flare  
216 1 1 Aura  
217 1 1 Ultima  
218 1 1 Triple  
219 1 1 Full-Life  
220 1 1 Meteor  
221 1 1 Holy  
222 1 1 Triple  
223 1 1 Aura  
224 1 1 Ultima  
225 1 1 Triple  
226 1 1 Full-Life  
227 1 1 Meteor  
228 1 1 Holy  
229 1 1 Flare  
230 1 1 Aura  
231 1 1 Ultima  
232 1 1 Triple  
233 1 1 Full-Life  
234 1 1 Meteor  
235 1 1 Triple  
236 1 1 Flare  
237 1 1 Aura  
238 1 1 Ultima  
239 1 1 Triple  
240 1 1 Full-Life  
241 1 1 Meteor  
242 1 1 Holy  
243 1 1 Flare  
244 1 1 Aura  
245 1 1 Ultima  
246 0 1 Blizzard  
247 0 1 Cure  
248 1 1 Dispel  
249 1 1 Confuse  
250 0 0 Meteor  
251 0 0 Double  
252 0 0 Aura  
253 0 0 Holy  
254 0 0 Flare  
255 0 0 Ultima  
256 1 1 Scan  
