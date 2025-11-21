---
layout: default
title: Field Opcodes
parent: Field
nav_order: 2
author:
  - Aali
  - myst6re
  - Shard
permalink: /technical-reference/field/field-opcodes/
---

## The language

The field script language in ff8 is a simple assembly language with a stack. Here is an example:

`stack =  []`

`PSHM_W              1024 # push  var1024  onto  the  stack  (stack =  [var1024])`  
`PSHN_L              6 # push  number  6  onto  the  stack  (stack =  [6Â ; var1024])`  
`CAL                    EQ # compare  the  two  numbers  at  the  top  of  the  stack, pop  this  numbers, and  push  the  result  (1  or  0)  into  the  stack  (stack =  [1  or  0])  `  
`JPF                    LABEL1 # if  the  popped  top  of  the  stack  is  0, jump  to  LABEL1  (stack =  [])`  
`PSHN_L              0 # push  0  at  the  top  of  the  stack  (stack =  [0])`  
`POPM_W              1024 # pop  the  top  of  the  stack  into  var1024  (stack =  [])`  
`JMP                    LABEL2 # goto  LABEL2`  
`LABEL1`  
`PSHN_L              1 # push  1  at  the  top  of  the  stack  (stack =  [1])`  
`POPM_W              1024 # pop  the  top  of  the  stack  into  var1024  (stack =  [])`  
`LABEL2`  
`...`

In standard code, it's equivalent to:

`if(var1024 == 6)  {`  
`        var1024 = 0;`  
`} else {`  
`        var1024 = 1;`  
`}`

## Reading Documentation

Each Opcode's page lists all the parameters for that function in the order you would put them on the stack before the function call. The inline argument is
listed separately, if the function requires one. For example, on the page for [SET3](01E_SET3), the parameters are listed like this:

*XCoord*

*YCoord*

*ZCoord*

**SET3**

Which means when you call **SET3**, the ZCoord is the top item on the stack, YCoord is under it, and XCoord is under that, for example

`PSHN_L            402      (XCoord)`  
`PSHN_L -381    (YCoord)`  
`PSHN_L            20        (ZCoord)`  
`SET3                17        (walkmesh  triangle  ID)`

## Opcode list

| Opcode | Name                                             | Function Type      |
|--------|--------------------------------------------------|--------------------|
| 000    | [000 NOP](000_NOP)*                              | Script Processing  |
| 001    | [001 CAL](001_CAL)                               | Script Processing  |
| 002    | [002 JMP](002_JMP)                               | Script Processing  |
| 003    | [003 JPF](003_JPF)                               | Script Processing  |
| 004    | [004 GJMP](Opcodes/004_GJMP)*                    | Script Processing  |
| 005    | [005 LBL](005_LBL)                               | Script Processing  |
| 006    | [006 RET](006_RET)                               | Script Processing  |
| 007    | [007 PSHN\_L](007_PSHN_L)                        | Memory             |
| 008    | [008 PSHI\_L](008_PSHI_L)                        | Memory             |
| 009    | [009 POPI\_L](009_POPI_L)                        | Memory             |
| 00A    | [00A PSHM\_B](00A_PSHM_B)                        | Memory             |
| 00B    | [00B POPM\_B](00B_POPM_B)                        | Memory             |
| 00C    | [00C PSHM\_W](00C_PSHM_W)                        | Memory             |
| 00D    | [00D POPM\_W](00D_POPM_W)                        | Memory             |
| 00E    | [00E PSHM\_L](00E_PSHM_L)                        | Memory             |
| 00F    | [00F POPM\_L](00F_POPM_L)                        | Memory             |
| 010    | [010 PSHSM\_B](010_PSHSM_B)                      | Memory             |
| 011    | [011 PSHSM\_W](011_PSHSM_W)                      | Memory             |
| 012    | [012 PSHSM\_L](012_PSHSM_L)                      | Memory             |
| 013    | [013 PSHAC](013_PSHAC)                           | Memory             |
| 014    | [014 REQ](014_REQ)                               | Script Processing  |
| 015    | [015 REQSW](015_REQSW)                           | Script Processing  |
| 016    | [016 REQEW](016_REQEW)                           | Script Processing  |
| 017    | [017 PREQ](017_PREQ)                             | Script Processing  |
| 018    | [018 PREQSW](018_PREQSW)                         | Script Processing  |
| 019    | [019 PREQEW](019_PREQEW)                         | Script Processing  |
| 01A    | [01A UNUSE](01A_UNUSE)                           | Entity             |
| 01B    | [01B DEBUG](01B_DEBUG)*                          |                    |
| 01C    | [01C HALT](01C_HALT)                             | Script Processing  |
| 01D    | [01D SET](01D_SET)                               | Entity             |
| 01E    | [01E SET3](01E_SET3)                             | Entity             |
| 01F    | [01F IDLOCK](01F_IDLOCK)                         | Field related      |
| 020    | [020 IDUNLOCK](020_IDUNLOCK)                     | Field related      |
| 021    | [021 EFFECTPLAY2](021_EFFECTPLAY2)               | Music and Sound    |
| 022    | [022 FOOTSTEP](022_FOOTSTEP)                     |                    |
| 023    | [023 JUMP](023_JUMP)                             | Entity             |
| 024    | [024 JUMP3](024_JUMP3)                           | Entity             |
| 025    | [025 LADDERUP](025_LADDERUP)                     | Entity             |
| 026    | [026 LADDERDOWN](026_LADDERDOWN)                 | Entity             |
| 027    | [027 LADDERUP2](027_LADDERUP2)                   | Entity             |
| 028    | [028 LADDERDOWN2](028_LADDERDOWN2)               | Entity             |
| 029    | [029 MAPJUMP](029_MAPJUMP)                       | Field related      |
| 02A    | [02A MAPJUMP3](02A_MAPJUMP3)                     | Field related      |
| 02B    | [02B SETMODEL](02B_SETMODEL)                     | Entity             |
| 02C    | [02C BASEANIME](02C_BASEANIME)                   | Animation          |
| 02D    | [02D ANIME](02D_ANIME)                           | Animation          |
| 02E    | [02E ANIMEKEEP](02E_ANIMEKEEP)                   | Animation          |
| 02F    | [02F CANIME](02F_CANIME)                         | Animation          |
| 030    | [030 CANIMEKEEP](030_CANIMEKEEP)                 | Animation          |
| 031    | [031 RANIME](031_RANIME)                         | Animation          |
| 032    | [032 RANIMEKEEP](032_RANIMEKEEP)                 | Animation          |
| 033    | [033 RCANIME](033_RCANIME)                       | Animation          |
| 034    | [034 RCANIMEKEEP](034_RCANIMEKEEP)               | Animation          |
| 035    | [035 RANIMELOOP](035_RANIMELOOP)                 | Animation          |
| 036    | [036 RCANIMELOOP](036_RCANIMELOOP)               | Animation          |
| 037    | [037 LADDERANIME](037_LADDERANIME)               | Animation          |
| 038    | [038 DISCJUMP](038_DISCJUMP)                     | Field related      |
| 039    | [039 SETLINE](039_SETLINE)                       | Entity             |
| 03A    | [03A LINEON](03A_LINEON)                         | Entity             |
| 03B    | [03B LINEOFF](03B_LINEOFF)                       | Entity             |
| 03C    | [03C WAIT](03C_WAIT)                             | Script Processing  |
| 03D    | [03D MSPEED](03D_MSPEED)                         |                    |
| 03E    | [03E MOVE](03E_MOVE)                             | Entity             |
| 03F    | [03F MOVEA](03F_MOVEA)                           |                    |
| 040    | [040 PMOVEA](040_PMOVEA)                         |                    |
| 041    | [041 CMOVE](041_CMOVE)                           |                    |
| 042    | [042 FMOVE](042_FMOVE)                           |                    |
| 043    | [043 PJUMPA](043_PJUMPA)                         |                    |
| 044    | [044 ANIMESYNC](044_ANIMESYNC)                   | Script Processing  |
| 045    | [045 ANIMESTOP](045_ANIMESTOP)                   | Animation          |
| 046    | [046 MESW](046_MESW)*                            |                    |
| 047    | [047 MES](047_MES)                               | Message            |
| 048    | [048 MESSYNC](048_MESSYNC)                       | Script Processing  |
| 049    | [049 MESVAR](049_MESVAR)                         | Message            |
| 04A    | [04A ASK](04A_ASK)                               | Message            |
| 04B    | [04B WINSIZE](04B_WINSIZE)                       | Message            |
| 04C    | [04C WINCLOSE](04C_WINCLOSE)                     | Message            |
| 04D    | [04D UCON](04D_UCON)                             | Misc               |
| 04E    | [04E UCOFF](04E_UCOFF)                           | Misc               |
| 04F    | [04F MOVIE](04F_MOVIE)                           | Movie              |
| 050    | [050 MOVIESYNC](050_MOVIESYNC)                   | Script Processing  |
| 051    | [051 SETPC](051_SETPC)                           | Party management   |
| 052    | [052 DIR](052_DIR)                               | Entity             |
| 053    | [053 DIRP](053_DIRP)                             |                    |
| 054    | [054 DIRA](054_DIRA)                             |                    |
| 055    | [055 PDIRA](055_PDIRA)                           |                    |
| 056    | [056 SPUREADY](056_SPUREADY)                     | Timer              |
| 057    | [057 TALKON](057_TALKON)                         | Entity             |
| 058    | [058 TALKOFF](058_TALKOFF)                       | Entity             |
| 059    | [059 PUSHON](059_PUSHON)                         | Entity             |
| 05A    | [05A PUSHOFF](05A_PUSHOFF)                       | Entity             |
| 05B    | [05B ISTOUCH](05B_ISTOUCH)                       |                    |
| 05C    | [05C MAPJUMPO](05C_MAPJUMPO)                     | Field related      |
| 05D    | [05D MAPJUMPON](05D_MAPJUMPON)                   | Field related      |
| 05E    | [05E MAPJUMPOFF](05E_MAPJUMPOFF)                 | Field related      |
| 05F    | [05F SETMESSPEED](05F_SETMESSPEED)               | Message            |
| 060    | [060 SHOW](060_SHOW)                             | Entity             |
| 061    | [061 HIDE](061_HIDE)                             | Entity             |
| 062    | [062 TALKRADIUS](062_TALKRADIUS)                 | Entity             |
| 063    | [063 PUSHRADIUS](063_PUSHRADIUS)                 | Entity             |
| 064    | [064 AMESW](064_AMESW)                           | Message            |
| 065    | [065 AMES](065_AMES)                             | Message            |
| 066    | [066 GETINFO](066_GETINFO)                       |                    |
| 067    | [067 THROUGHON](067_THROUGHON)                   | Entity             |
| 068    | [068 THROUGHOFF](068_THROUGHOFF)                 | Entity             |
| 069    | [069 BATTLE](069_BATTLE)                         | Battle             |
| 06A    | [06A BATTLERESULT](06A_BATTLERESULT)             | Battle             |
| 06B    | [06B BATTLEON](06B_BATTLEON)                     | Field related      |
| 06C    | [06C BATTLEOFF](06C_BATTLEOFF)                   | Field related      |
| 06D    | [06D KEYSCAN](06D_KEYSCAN)                       | Input              |
| 06E    | [06E KEYON](06E_KEYON)                           | Input              |
| 06F    | [06F AASK](06F_AASK)                             | Message            |
| 070    | [070 PGETINFO](070_PGETINFO)                     |                    |
| 071    | [071 DSCROLL](071_DSCROLL)                       |                    |
| 072    | [072 LSCROLL](072_LSCROLL)                       |                    |
| 073    | [073 CSCROLL](073_CSCROLL)                       |                    |
| 074    | [074 DSCROLLA](074_DSCROLLA)                     |                    |
| 075    | [075 LSCROLLA](Opcodes/075_LSCROLLA)             |                    |
| 076    | [076 CSCROLLA](Opcodes/076_CSCROLLA)             |                    |
| 077    | [077 SCROLLSYNC](077_SCROLLSYNC)                 | Script Processing  |
| 078    | [078 RMOVE](Opcodes/078_RMOVE)                   |                    |
| 079    | [079 RMOVEA](Opcodes/079_RMOVEA)                 |                    |
| 07A    | [07A RPMOVEA](Opcodes/07A_RPMOVEA)               |                    |
| 07B    | [07B RCMOVE](Opcodes/07B_RCMOVE)                 |                    |
| 07C    | [07C RFMOVE](Opcodes/07C_RFMOVE)                 |                    |
| 07D    | [07D MOVESYNC](07D_MOVESYNC)                     | Script Processing  |
| 07E    | [07E CLEAR](07E_CLEAR)                           | Field related      |
| 07F    | [07F DSCROLLP](Opcodes/07F_DSCROLLP)             |                    |
| 080    | [080 LSCROLLP](Opcodes/080_LSCROLLP)             |                    |
| 081    | [081 CSCROLLP](Opcodes/081_CSCROLLP)             |                    |
| 082    | [082 LTURNR](Opcodes/082_LTURNR)                 |                    |
| 083    | [083 LTURNL](Opcodes/083_LTURNL)                 |                    |
| 084    | [084 CTURNR](084_CTURNR)                         |                    |
| 085    | [085 CTURNL](085_CTURNL)                         |                    |
| 086    | [086 ADDPARTY](086_ADDPARTY)                     | Party Management   |
| 087    | [087 SUBPARTY](087_SUBPARTY)                     | Party Management   |
| 088    | [088 CHANGEPARTY](Opcodes/088_CHANGEPARTY)       | Party Management   |
| 089    | [089 REFRESHPARTY](Opcodes/089_REFRESHPARTY)     | Party Management   |
| 08A    | [08A SETPARTY](08A_SETPARTY)                     | Party Management   |
| 08B    | [08B ISPARTY](08B_ISPARTY)                       | Party Management   |
| 08C    | [08C ADDMEMBER](08C_ADDMEMBER)                   | Party Management   |
| 08D    | [08D SUBMEMBER](08D_SUBMEMBER)                   | Party Management   |
| 08E    | [08E ISMEMBER](Opcodes/08E_ISMEMBER)*            | Party Management   |
| 08F    | [08F LTURN](Opcodes/08F_LTURN)                   |                    |
| 090    | [090 CTURN](090_CTURN)                           |                    |
| 091    | [091 PLTURN](Opcodes/091_PLTURN)                 |                    |
| 092    | [092 PCTURN](092_PCTURN)                         |                    |
| 093    | [093 JOIN](093_JOIN)                             | Entity             |
| 094    | [094 MESFORCUS](Opcodes/094_MESFORCUS)*          |                    |
| 095    | [095 BGANIME](095_BGANIME)                       | Field related      |
| 096    | [096 RBGANIME](Opcodes/096_RBGANIME)             | Field related      |
| 097    | [097 RBGANIMELOOP](Opcodes/097_RBGANIMELOOP)     | Field related      |
| 098    | [098 BGANIMESYNC](Opcodes/098_BGANIMESYNC)       | Field related      |
| 099    | [099 BGDRAW](Opcodes/099_BGDRAW)                 | Field related      |
| 09A    | [09A BGOFF](Opcodes/09A_BGOFF)                   | Field related      |
| 09B    | [09B BGANIMESPEED](Opcodes/09B_BGANIMESPEED)     | Field related      |
| 09C    | [09C SETTIMER](09C_SETTIMER)                     | Timer              |
| 09D    | [09D DISPTIMER](09D_DISPTIMER)                   | Timer              |
| 09E    | [09E SHADETIMER](Opcodes/09E_SHADETIMER)*        |                    |
| 09F    | [09F SETGETA](09F_SETGETA)                       |                    |
| 0A0    | [0A0 SETROOTTRANS](Opcodes/0A0_SETROOTTRANS)     |                    |
| 0A1    | [0A1 SETVIBRATE](0A1_SETVIBRATE)                 |                    |
| 0A2    | [0A2 STOPVIBRATE](Opcodes/0A2_STOPVIBRATE)*      |                    |
| 0A3    | [0A3 MOVIEREADY](0A3_MOVIEREADY)                 | Movie              |
| 0A4    | [0A4 GETTIMER](Opcodes/0A4_GETTIMER)             | Timer              |
| 0A5    | [0A5 FADEIN](Opcodes/0A5_FADEIN)                 | Field related      |
| 0A6    | [0A6 FADEOUT](Opcodes/0A6_FADEOUT)               | Field related      |
| 0A7    | [0A7 FADESYNC](Opcodes/0A7_FADESYNC)             | Script Processing  |
| 0A8    | [0A8 SHAKE](Opcodes/0A8_SHAKE)                   | Field related      |
| 0A9    | [0A9 SHAKEOFF](Opcodes/0A9_SHAKEOFF)             | Field related      |
| 0AA    | [0AA FADEBLACK](0AA_FADEBLACK)                   | Field related      |
| 0AB    | [0AB FOLLOWOFF](Opcodes/0AB_FOLLOWOFF)           |                    |
| 0AC    | [0AC FOLLOWON](Opcodes/0AC_FOLLOWON)             |                    |
| 0AD    | [0AD GAMEOVER](0AD_GAMEOVER)                     | Field related      |
| 0AE    | [0AE ENDING](Opcodes/0AE_ENDING)*                |                    |
| 0AF    | [0AF SHADELEVEL](0AF_SHADELEVEL)                 |                    |
| 0B0    | [0B0 SHADEFORM](Opcodes/0B0_SHADEFORM)           |                    |
| 0B1    | [0B1 FMOVEA](Opcodes/0B1_FMOVEA)                 |                    |
| 0B2    | [0B2 FMOVEP](Opcodes/0B2_FMOVEP)                 |                    |
| 0B3    | [0B3 SHADESET](Opcodes/0B3_SHADESET)             |                    |
| 0B4    | [0B4 MUSICCHANGE](0B4_MUSICCHANGE)               | Music and Sound    |
| 0B5    | [0B5 MUSICLOAD](0B5_MUSICLOAD)                   | Music and Sound    |
| 0B6    | [0B6 FADENONE](Opcodes/0B6_FADENONE)             |                    |
| 0B7    | [0B7 POLYCOLOR](Opcodes/0B7_POLYCOLOR)           |                    |
| 0B8    | [0B8 POLYCOLORALL](Opcodes/0B8_POLYCOLORALL)     |                    |
| 0B9    | [0B9 KILLTIMER](Opcodes/0B9_KILLTIMER)           | Timer              |
| 0BA    | [0BA CROSSMUSIC](Opcodes/0BA_CROSSMUSIC)         |                    |
| 0BB    | [0BB DUALMUSIC](Opcodes/0BB_DUALMUSIC)           |                    |
| 0BC    | [0BC EFFECTPLAY](0BC_EFFECTPLAY)                 | Music and Sound    |
| 0BD    | [0BD EFFECTLOAD](0BD_EFFECTLOAD)                 | Music and Sound    |
| 0BE    | [0BE LOADSYNC](Opcodes/0BE_LOADSYNC)             |                    |
| 0BF    | [0BF MUSICSTOP](0BF_MUSICSTOP)                   | Music and Sound    |
| 0C0    | [0C0 MUSICVOL](0C0_MUSICVOL)                     | Music and Sound    |
| 0C1    | [0C1 MUSICVOLTRANS](0C1_MUSICVOLTRANS)           | Music and Sound    |
| 0C2    | [0C2 MUSICVOLFADE](Opcodes/0C2_MUSICVOLFADE)     | Music and Sound    |
| 0C3    | [0C3 ALLSEVOL](0C3_ALLSEVOL)                     | Music and Sound    |
| 0C4    | [0C4 ALLSEVOLTRANS](0C4_ALLSEVOLTRANS)           | Music and Sound    |
| 0C5    | [0C5 ALLSEPOS](0C5_ALLSEPOS)*                    | Music and Sound    |
| 0C6    | [0C6 ALLSEPOSTRANS](0C6_ALLSEPOSTRANS)           | Music and Sound    |
| 0C7    | [0C7 SEVOL](0C7_SEVOL)                           | Music and Sound    |
| 0C8    | [0C8 SEVOLTRANS](0C8_SEVOLTRANS)                 | Music and Sound    |
| 0C9    | [0C9 SEPOS](0C9_SEPOS)                           | Music and Sound    |
| 0CA    | [0CA SEPOSTRANS](0CA_SEPOSTRANS)                 | Music and Sound    |
| 0CB    | [0CB SETBATTLEMUSIC](0CB_SETBATTLEMUSIC)         | Music and Sound    |
| 0CC    | [0CC BATTLEMODE](0CC_BATTLEMODE)                 | Battle             |
| 0CD    | [0CD SESTOP](0CD_SESTOP)                         | Music and Sound    |
| 0CE    | [0CE BGANIMEFLAG](Opcodes/0CE_BGANIMEFLAG)*      |                    |
| 0CF    | [0CF INITSOUND](Opcodes/0CF_INITSOUND)           |                    |
| 0D0    | [0D0 BGSHADE](Opcodes/0D0_BGSHADE)               |                    |
| 0D1    | [0D1 BGSHADESTOP](Opcodes/0D1_BGSHADESTOP)       |                    |
| 0D2    | [0D2 RBGSHADELOOP](Opcodes/0D2_RBGSHADELOOP)     |                    |
| 0D3    | [0D3 DSCROLL2](Opcodes/0D3_DSCROLL2)             |                    |
| 0D4    | [0D4 LSCROLL2](Opcodes/0D4_LSCROLL2)             |                    |
| 0D5    | [0D5 CSCROLL2](Opcodes/0D5_CSCROLL2)             |                    |
| 0D6    | [0D6 DSCROLLA2](Opcodes/0D6_DSCROLLA2)           |                    |
| 0D7    | [0D7 LSCROLLA2](Opcodes/0D7_LSCROLLA2)*          |                    |
| 0D8    | [0D8 CSCROLLA2](Opcodes/0D8_CSCROLLA2)           |                    |
| 0D9    | [0D9 DSCROLLP2](Opcodes/0D9_DSCROLLP2)*          |                    |
| 0DA    | [0DA LSCROLLP2](Opcodes/0DA_LSCROLLP2)*          |                    |
| 0DB    | [0DB CSCROLLP2](Opcodes/0DB_CSCROLLP2)*          |                    |
| 0DC    | [0DC SCROLLSYNC2](Opcodes/0DC_SCROLLSYNC2)       |                    |
| 0DD    | [0DD SCROLLMODE2](Opcodes/0DD_SCROLLMODE2)       |                    |
| 0DE    | [0DE MENUENABLE](Opcodes/0DE_MENUENABLE)         | Menus              |
| 0DF    | [0DF MENUDISABLE](Opcodes/0DF_MENUDISABLE)       | Menus              |
| 0E0    | [0E0 FOOTSTEPON](Opcodes/0E0_FOOTSTEPON)         |                    |
| 0E1    | [0E1 FOOTSTEPOFF](Opcodes/0E1_FOOTSTEPOFF)       |                    |
| 0E2    | [0E2 FOOTSTEPOFFALL](Opcodes/0E2_FOOTSTEPOFFALL) |                    |
| 0E3    | [0E3 FOOTSTEPCUT](Opcodes/0E3_FOOTSTEPCUT)       |                    |
| 0E4    | [0E4 PREMAPJUMP](Opcodes/0E4_PREMAPJUMP)         |                    |
| 0E5    | [0E5 USE](0E5_USE)                               | Entity             |
| 0E6    | [0E6 SPLIT](0E6_SPLIT)                           | Entity             |
| 0E7    | [0E7 ANIMESPEED](0E7_ANIMESPEED)                 | Animation          |
| 0E8    | [0E8 RND](0E8_RND)                               |                    |
| 0E9    | [0E9 DCOLADD](Opcodes/0E9_DCOLADD)               |                    |
| 0EA    | [0EA DCOLSUB](Opcodes/0EA_DCOLSUB)               |                    |
| 0EB    | [0EB TCOLADD](Opcodes/0EB_TCOLADD)               |                    |
| 0EC    | [0EC TCOLSUB](Opcodes/0EC_TCOLSUB)               |                    |
| 0ED    | [0ED FCOLADD](Opcodes/0ED_FCOLADD)               | Field related      |
| 0EE    | [0EE FCOLSUB](0EE_FCOLSUB)                       | Field related      |
| 0EF    | [0EF COLSYNC](Opcodes/0EF_COLSYNC)               | Script processing  |
| 0F0    | [0F0 DOFFSET](Opcodes/0F0_DOFFSET)               |                    |
| 0F1    | [0F1 LOFFSETS](Opcodes/0F1_LOFFSETS)             |                    |
| 0F2    | [0F2 COFFSETS](Opcodes/0F2_COFFSETS)             |                    |
| 0F3    | [0F3 LOFFSET](Opcodes/0F3_LOFFSET)               |                    |
| 0F4    | [0F4 COFFSET](Opcodes/0F4_COFFSET)               |                    |
| 0F5    | [0F5 OFFSETSYNC](Opcodes/0F5_OFFSETSYNC)         |                    |
| 0F6    | [0F6 RUNENABLE](0F6_RUNENABLE)                   | Entity             |
| 0F7    | [0F7 RUNDISABLE](0F7_RUNDISABLE)                 | Entity             |
| 0F8    | [0F8 MAPFADEOFF](Opcodes/0F8_MAPFADEOFF)         | Field related      |
| 0F9    | [0F9 MAPFADEON](Opcodes/0F9_MAPFADEON)           | Field related      |
| 0FA    | [0FA INITTRACE](Opcodes/0FA_INITTRACE)           |                    |
| 0FB    | [0FB SETDRESS](Opcodes/0FB_SETDRESS)             | Entity             |
| 0FC    | [0FC GETDRESS](Opcodes/0FC_GETDRESS)*            | Entity             |
| 0FD    | [0FD FACEDIR](Opcodes/0FD_FACEDIR)               | Entity             |
| 0FE    | [0FE FACEDIRA](0FE_FACEDIRA)                     |                    |
| 0FF    | [0FF FACEDIRP](0FF_FACEDIRP)                     |                    |
| 100    | [100 FACEDIRLIMIT](100_FACEDIRLIMIT)             |                    |
| 101    | [101 FACEDIROFF](101_FACEDIROFF)                 |                    |
| 102    | [102 SARALYOFF](102_SARALYOFF)                   |                    |
| 103    | [103 SARALYON](103_SARALYON)                     |                    |
| 104    | [104 SARALYDISPOFF](104_SARALYDISPOFF)           |                    |
| 105    | [105 SARALYDISPON](105_SARALYDISPON)             |                    |
| 106    | [106 MESMODE](106_MESMODE)                       | Message            |
| 107    | [107 FACEDIRINIT](107_FACEDIRINIT)               |                    |
| 108    | [108 FACEDIRI](Opcodes/108_FACEDIRI)             |                    |
| 109    | [109 JUNCTION](109_JUNCTION)                     | Party Management   |
| 10A    | [10A SETCAMERA](Opcodes/10A_SETCAMERA)           | Field related      |
| 10B    | [10B BATTLECUT](10B_BATTLECUT)                   |                    |
| 10C    | [10C FOOTSTEPCOPY](Opcodes/10C_FOOTSTEPCOPY)     |                    |
| 10D    | [10D WORLDMAPJUMP](10D_WORLDMAPJUMP)             | Field related      |
| 10E    | [10E RFACEDIRI](Opcodes/10E_RFACEDIRI)*          |                    |
| 10F    | [10F RFACEDIR](Opcodes/10F_RFACEDIR)             |                    |
| 110    | [110 RFACEDIRA](Opcodes/110_RFACEDIRA)           |                    |
| 111    | [111 RFACEDIRP](Opcodes/111_RFACEDIRP)           |                    |
| 112    | [112 RFACEDIROFF](Opcodes/112_RFACEDIROFF)       |                    |
| 113    | [113 FACEDIRSYNC](Opcodes/113_FACEDIRSYNC)       |                    |
| 114    | [114 COPYINFO](Opcodes/114_COPYINFO)             |                    |
| 115    | [115 PCOPYINFO](Opcodes/115_PCOPYINFO)*          |                    |
| 116    | [116 RAMESW](116_RAMESW)                         | Message            |
| 117    | [117 BGSHADEOFF](Opcodes/117_BGSHADEOFF)         | Field related      |
| 118    | [118 AXIS](Opcodes/118_AXIS)                     |                    |
| 119    | [119 AXISSYNC](Opcodes/119_AXISSYNC)*            |                    |
| 11A    | [11A MENUNORMAL](11A_MENUNORMAL)                 | Menus              |
| 11B    | [11B MENUPHS](11B_MENUPHS)                       | Menus              |
| 11C    | [11C BGCLEAR](Opcodes/11C_BGCLEAR)               |                    |
| 11D    | [11D GETPARTY](11D_GETPARTY)                     | Party Management   |
| 11E    | [11E MENUSHOP](Opcodes/11E_MENUSHOP)             | Menus              |
| 11F    | [11F DISC](11F_DISC)                             | Field related      |
| 120    | [120 DSCROLL3](Opcodes/120_DSCROLL3)*            |                    |
| 121    | [121 LSCROLL3](Opcodes/121_LSCROLL3)             |                    |
| 122    | [122 CSCROLL3](Opcodes/122_CSCROLL3)             |                    |
| 123    | [123 MACCEL](Opcodes/123_MACCEL)                 |                    |
| 124    | [124 MLIMIT](Opcodes/124_MLIMIT)                 |                    |
| 125    | [125 ADDITEM](125_ADDITEM)                       | Item/Magic/Card/GF |
| 126    | [126 SETWITCH](126_SETWITCH)                     |                    |
| 127    | [127 SETODIN](127_SETODIN)                       |                    |
| 128    | [128 RESETGF](Opcodes/128_RESETGF)               |                    |
| 129    | [129 MENUNAME](129_MENUNAME)                     | Menus              |
| 12A    | [12A REST](Opcodes/12A_REST)                     |                    |
| 12B    | [12B MOVECANCEL](Opcodes/12B_MOVECANCEL)         |                    |
| 12C    | [12C PMOVECANCEL](Opcodes/12C_PMOVECANCEL)*      |                    |
| 12D    | [12D ACTORMODE](12D_ACTORMODE)                   |                    |
| 12E    | [12E MENUSAVE](12E_MENUSAVE)                     | Menus              |
| 12F    | [12F SAVEENABLE](12F_SAVEENABLE)                 | Menus              |
| 130    | [130 PHSENABLE](130_PHSENABLE)                   | Menus              |
| 131    | [131 HOLD](131_HOLD)                             | Party Management   |
| 132    | [132 MOVIECUT](132_MOVIECUT)                     |                    |
| 133    | [133 SETPLACE](133_SETPLACE)                     |                    |
| 134    | [134 SETDCAMERA](Opcodes/134_SETDCAMERA)         |                    |
| 135    | [135 CHOICEMUSIC](Opcodes/135_CHOICEMUSIC)       |                    |
| 136    | [136 GETCARD](Opcodes/136_GETCARD)               |                    |
| 137    | [137 DRAWPOINT](137_DRAWPOINT)                   | Menus              |
| 138    | [138 PHSPOWER](138_PHSPOWER)                     |                    |
| 139    | [139 KEY](Opcodes/139_KEY)                       |                    |
| 13A    | [13A CARDGAME](13A_CARDGAME)                     | Menus              |
| 13B    | [13B SETBAR](Opcodes/13B_SETBAR)                 |                    |
| 13C    | [13C DISPBAR](Opcodes/13C_DISPBAR)               |                    |
| 13D    | [13D KILLBAR](Opcodes/13D_KILLBAR)               |                    |
| 13E    | [13E SCROLLRATIO2](Opcodes/13E_SCROLLRATIO2)     |                    |
| 13F    | [13F WHOAMI](13F_WHOAMI)                         |                    |
| 140    | [140 MUSICSTATUS](Opcodes/140_MUSICSTATUS)       |                    |
| 141    | [141 MUSICREPLAY](Opcodes/141_MUSICREPLAY)       |                    |
| 142    | [142 DOORLINEOFF](Opcodes/142_DOORLINEOFF)       | Entity             |
| 143    | [143 DOORLINEON](Opcodes/143_DOORLINEON)         | Entity             |
| 144    | [144 MUSICSKIP](Opcodes/144_MUSICSKIP)           |                    |
| 145    | [145 DYING](145_DYING)                           | Party Management   |
| 146    | [146 SETHP](Opcodes/146_SETHP)                   | Party Management   |
| 147    | [147 GETHP](Opcodes/147_GETHP)*                  | Party Management   |
| 148    | [148 MOVEFLUSH](148_MOVEFLUSH)                   |                    |
| 149    | [149 MUSICVOLSYNC](Opcodes/149_MUSICVOLSYNC)     |                    |
| 14A    | [14A PUSHANIME](Opcodes/14A_PUSHANIME)           |                    |
| 14B    | [14B POPANIME](Opcodes/14B_POPANIME)             |                    |
| 14C    | [14C KEYSCAN2](Opcodes/14C_KEYSCAN2)             | Input              |
| 14D    | [14D KEYON2](Opcodes/14D_KEYON2)*                | Input              |
| 14E    | [14E PARTICLEON](Opcodes/14E_PARTICLEON)         |                    |
| 14F    | [14F PARTICLEOFF](Opcodes/14F_PARTICLEOFF)       |                    |
| 150    | [150 KEYSIGHNCHANGE](150_KEYSIGHNCHANGE)         |                    |
| 151    | [151 ADDGIL](Opcodes/151_ADDGIL)                 | Item/Magic/Card/GF |
| 152    | [152 ADDPASTGIL](Opcodes/152_ADDPASTGIL)         | Item/Magic/Card/GF |
| 153    | [153 ADDSEEDLEVEL](153_ADDSEEDLEVEL)             | Item/Magic/Card/GF |
| 154    | [154 PARTICLESET](Opcodes/154_PARTICLESET)       |                    |
| 155    | [155 SETDRAWPOINT](155_SETDRAWPOINT)             |                    |
| 156    | [156 MENUTIPS](Opcodes/156_MENUTIPS)             | Menus              |
| 157    | [157 LASTIN](157_LASTIN)                         |                    |
| 158    | [158 LASTOUT](158_LASTOUT)                       |                    |
| 159    | [159 SEALEDOFF](159_SEALEDOFF)                   |                    |
| 15A    | [15A MENUTUTO](Opcodes/15A_MENUTUTO)             | Menus              |
| 15B    | [15B OPENEYES](Opcodes/15B_OPENEYES)*            |                    |
| 15C    | [15C CLOSEEYES](Opcodes/15C_CLOSEEYES)           |                    |
| 15D    | [15D BLINKEYES](Opcodes/15D_BLINKEYES)*          |                    |
| 15E    | [15E SETCARD](15E_SETCARD)                       | Item/Magic/Card/GF |
| 15F    | [15F HOWMANYCARD](Opcodes/15F_HOWMANYCARD)       | Item/Magic/Card/GF |
| 160    | [160 WHERECARD](Opcodes/160_WHERECARD)           | Item/Magic/Card/GF |
| 161    | [161 ADDMAGIC](161_ADDMAGIC)                     | Item/Magic/Card/GF |
| 162    | [162 SWAP](Opcodes/162_SWAP)                     |                    |
| 163    | [163 SETPARTY2](Opcodes/163_SETPARTY2)*          |                    |
| 164    | [164 SPUSYNC](164_SPUSYNC)                       | Timer              |
| 165    | [165 BROKEN](Opcodes/165_BROKEN)                 |                    |
| 166    | [166 UNKNOWN1](166_UNKNOWN1)                     |                    |
| 167    | [167 UNKNOWN2](Opcodes/167_UNKNOWN2)             |                    |
| 168    | [168 UNKNOWN3](Opcodes/168_UNKNOWN3)             |                    |
| 169    | [169 UNKNOWN4](169_UNKNOWN4)                     |                    |
| 170    | [170 UNKNOWN5](170_UNKNOWN5)                     | Item/Magic/Card/GF |
| 171    | [171 UNKNOWN6](171_UNKNOWN6)                     | Animation          |
| 172    | [172 UNKNOWN7](172_UNKNOWN7)                     | Animation          |
| 173    | [173 UNKNOWN8](173_UNKNOWN8)                     | Animation          |
| 174    | [174 UNKNOWN9](174_UNKNOWN9)                     | Animation          |
| 175    | [175 UNKNOWN10](175_UNKNOWN10)                   |                    |
| 176    | [176 UNKNOWN11](176_UNKNOWN11)                   |                    |
| 177    | [177 UNKNOWN12](177_UNKNOWN12)                   |                    |
| 178    | [178 UNKNOWN13](178_UNKNOWN13)                   | Music and Sound    |
| 179    | [179 UNKNOWN14](179_UNKNOWN14)                   | Music and Sound    |
| 180    | [180 UNKNOWN15](180_UNKNOWN15)                   |                    |
| 181    | [181 UNKNOWN16](181_UNKNOWN16)                   | Field related      |
| 182    | [182 UNKNOWN17](182_UNKNOWN17)                   | Field related      |
| 183    | [183 UNKNOWN18](183_UNKNOWN18)                   | Menus              |
