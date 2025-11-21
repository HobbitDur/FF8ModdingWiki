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

{: .no_toc }

## The language

The field script language in ff8 is a simple assembly language with a stack. Here is an example:

```
stack =  []

PSHM_W              1024 # push  var1024  onto  the  stack  (stack =  [var1024])  
PSHN_L              6 # push  number  6  onto  the  stack  (stack =  [6Â ; var1024])  
CAL                    EQ # compare  the  two  numbers  at  the  top  of  the  stack, pop  this  numbers, and  push  the  result  (1  or  0)  into  the  stack  (stack =  [1  or  0])    
JPF                    LABEL1 # if  the  popped  top  of  the  stack  is  0, jump  to  LABEL1  (stack =  [])  
PSHN_L              0 # push  0  at  the  top  of  the  stack  (stack =  [0])  
POPM_W              1024 # pop  the  top  of  the  stack  into  var1024  (stack =  [])  
JMP                    LABEL2 # goto  LABEL2  
LABEL1  
PSHN_L              1 # push  1  at  the  top  of  the  stack  (stack =  [1])  
POPM_W              1024 # pop  the  top  of  the  stack  into  var1024  (stack =  [])  
LABEL2  
...
```

In standard code, it's equivalent to:

```
if(var1024 == 6)  {  
        var1024 = 0;  
} else {  
        var1024 = 1;  
}
```

## Reading Documentation

Each Opcode's page lists all the parameters for that function in the order you would put them on the stack before the function call. The inline argument is
listed separately, if the function requires one. For example, on the page for [SET3](01E_set3), the parameters are listed like this:

*XCoord*

*YCoord*

*ZCoord*

**SET3**

Which means when you call **SET3**, the ZCoord is the top item on the stack, YCoord is under it, and XCoord is under that, for example

```
PSHN_L            402      (XCoord)
PSHN_L -381    (YCoord)  
PSHN_L            20        (ZCoord)  
SET3                17        (walkmesh  triangle  ID)
```

## Opcode list

| Opcode | Name                                     | Function Type      |
|--------|------------------------------------------|--------------------|
| 000    | [000 NOP](000_nop)                       | Script Processing  |
| 001    | [001 CAL](001_cal)                       | Script Processing  |
| 002    | [002 JMP](002_jmp)                       | Script Processing  |
| 003    | [003 JPF](003_jpf)                       | Script Processing  |
| 004    | [004 GJMP](004_gjmp)                     | Script Processing  |
| 005    | [005 LBL](005_lbl)                       | Script Processing  |
| 006    | [006 RET](006_ret)                       | Script Processing  |
| 007    | [007 PSHN_L](007_pshn_l)                 | Memory             |
| 008    | [008 PSHI_L](008_pshi_l)                 | Memory             |
| 009    | [009 POPI_L](009_popi_l)                 | Memory             |
| 00A    | [00A PSHM_B](00a_pshm_b)                 | Memory             |
| 00B    | [00B POPM_B](00b_popm_b)                 | Memory             |
| 00C    | [00C PSHM_W](00c_pshm_w)                 | Memory             |
| 00D    | [00D POPM_W](00d_popm_w)                 | Memory             |
| 00E    | [00E PSHM_L](00e_pshm_l)                 | Memory             |
| 00F    | [00F POPM_L](00f_popm_l)                 | Memory             |
| 010    | [010 PSHSM_B](010_pshsm_b)               | Memory             |
| 011    | [011 PSHSM_W](011_pshsm_w)               | Memory             |
| 012    | [012 PSHSM_L](012_pshsm_l)               | Memory             |
| 013    | [013 PSHAC](013_pshac)                   | Memory             |
| 014    | [014 REQ](014_req)                       | Script Processing  |
| 015    | [015 REQSW](015_reqsw)                   | Script Processing  |
| 016    | [016 REQEW](016_reqew)                   | Script Processing  |
| 017    | [017 PREQ](017_preq)                     | Script Processing  |
| 018    | [018 PREQSW](018_preqsw)                 | Script Processing  |
| 019    | [019 PREQEW](019_preqew)                 | Script Processing  |
| 01A    | [01A UNUSE](01a_unuse)                   | Entity             |
| 01B    | [01B DEBUG](01b_debug)                   |                    |
| 01C    | [01C HALT](01c_halt)                     | Script Processing  |
| 01D    | [01D SET](01d_set)                       | Entity             |
| 01E    | [01E SET3](01e_set3)                     | Entity             |
| 01F    | [01F IDLOCK](01f_idlock)                 | Field related      |
| 020    | [020 IDUNLOCK](020_idunlock)             | Field related      |
| 021    | [021 EFFECTPLAY2](021_effectplay2)       | Music and Sound    |
| 022    | [022 FOOTSTEP](022_footstep)             |                    |
| 023    | [023 JUMP](023_jump)                     | Entity             |
| 024    | [024 JUMP3](024_jump3)                   | Entity             |
| 025    | [025 LADDERUP](025_ladderup)             | Entity             |
| 026    | [026 LADDERDOWN](026_ladderdown)         | Entity             |
| 027    | [027 LADDERUP2](027_ladderup2)           | Entity             |
| 028    | [028 LADDERDOWN2](028_ladderdown2)       | Entity             |
| 029    | [029 MAPJUMP](029_mapjump)               | Field related      |
| 02A    | [02A MAPJUMP3](02a_mapjump3)             | Field related      |
| 02B    | [02B SETMODEL](02b_setmodel)             | Entity             |
| 02C    | [02C BASEANIME](02c_baseanime)           | Animation          |
| 02D    | [02D ANIME](02d_anime)                   | Animation          |
| 02E    | [02E ANIMEKEEP](02e_animekeep)           | Animation          |
| 02F    | [02F CANIME](02f_canime)                 | Animation          |
| 030    | [030 CANIMEKEEP](030_canimekeep)         | Animation          |
| 031    | [031 RANIME](031_ranime)                 | Animation          |
| 032    | [032 RANIMEKEEP](032_ranimekeep)         | Animation          |
| 033    | [033 RCANIME](033_rcanime)               | Animation          |
| 034    | [034 RCANIMEKEEP](034_rcanimekeep)       | Animation          |
| 035    | [035 RANIMELOOP](035_ranimeloop)         | Animation          |
| 036    | [036 RCANIMELOOP](036_rcanimeloop)       | Animation          |
| 037    | [037 LADDERANIME](037_ladderanime)       | Animation          |
| 038    | [038 DISCJUMP](038_discjump)             | Field related      |
| 039    | [039 SETLINE](039_setline)               | Entity             |
| 03A    | [03A LINEON](03a_lineon)                 | Entity             |
| 03B    | [03B LINEOFF](03b_lineoff)               | Entity             |
| 03C    | [03C WAIT](03c_wait)                     | Script Processing  |
| 03D    | [03D MSPEED](03d_mspeed)                 |                    |
| 03E    | [03E MOVE](03e_move)                     | Entity             |
| 03F    | [03F MOVEA](03f_movea)                   |                    |
| 040    | [040 PMOVEA](040_pmovea)                 |                    |
| 041    | [041 CMOVE](041_cmove)                   |                    |
| 042    | [042 FMOVE](042_fmove)                   |                    |
| 043    | [043 PJUMPA](043_pjumpa)                 |                    |
| 044    | [044 ANIMESYNC](044_animesync)           | Script Processing  |
| 045    | [045 ANIMESTOP](045_animestop)           | Animation          |
| 046    | [046 MESW](046_mesw)                     |                    |
| 047    | [047 MES](047_mes)                       | Message            |
| 048    | [048 MESSYNC](048_messync)               | Script Processing  |
| 049    | [049 MESVAR](049_mesvar)                 | Message            |
| 04A    | [04A ASK](04a_ask)                       | Message            |
| 04B    | [04B WINSIZE](04b_winsize)               | Message            |
| 04C    | [04C WINCLOSE](04c_winclose)             | Message            |
| 04D    | [04D UCON](04d_ucon)                     | Misc               |
| 04E    | [04E UCOFF](04e_ucoff)                   | Misc               |
| 04F    | [04F MOVIE](04f_movie)                   | Movie              |
| 050    | [050 MOVIESYNC](050_moviesync)           | Script Processing  |
| 051    | [051 SETPC](051_setpc)                   | Party management   |
| 052    | [052 DIR](052_dir)                       | Entity             |
| 053    | [053 DIRP](053_dirp)                     |                    |
| 054    | [054 DIRA](054_dira)                     |                    |
| 055    | [055 PDIRA](055_pdira)                   |                    |
| 056    | [056 SPUREADY](056_spuready)             | Timer              |
| 057    | [057 TALKON](057_talkon)                 | Entity             |
| 058    | [058 TALKOFF](058_talkoff)               | Entity             |
| 059    | [059 PUSHON](059_pushon)                 | Entity             |
| 05A    | [05A PUSHOFF](05a_pushoff)               | Entity             |
| 05B    | [05B ISTOUCH](05b_istouch)               |                    |
| 05C    | [05C MAPJUMPO](05c_mapjumpo)             | Field related      |
| 05D    | [05D MAPJUMPON](05d_mapjumpon)           | Field related      |
| 05E    | [05E MAPJUMPOFF](05e_mapjumpoff)         | Field related      |
| 05F    | [05F SETMESSPEED](05f_setmesspeed)       | Message            |
| 060    | [060 SHOW](060_show)                     | Entity             |
| 061    | [061 HIDE](061_hide)                     | Entity             |
| 062    | [062 TALKRADIUS](062_talkradius)         | Entity             |
| 063    | [063 PUSHRADIUS](063_pushradius)         | Entity             |
| 064    | [064 AMESW](064_amesw)                   | Message            |
| 065    | [065 AMES](065_ames)                     | Message            |
| 066    | [066 GETINFO](066_getinfo)               |                    |
| 067    | [067 THROUGHON](067_throughon)           | Entity             |
| 068    | [068 THROUGHOFF](068_throughoff)         | Entity             |
| 069    | [069 BATTLE](069_battle)                 | Battle             |
| 06A    | [06A BATTLERESULT](06a_battleresult)     | Battle             |
| 06B    | [06B BATTLEON](06b_battleon)             | Field related      |
| 06C    | [06C BATTLEOFF](06c_battleoff)           | Field related      |
| 06D    | [06D KEYSCAN](06d_keyscan)               | Input              |
| 06E    | [06E KEYON](06e_keyon)                   | Input              |
| 06F    | [06F AASK](06f_aask)                     | Message            |
| 070    | [070 PGETINFO](070_pgetinfo)             |                    |
| 071    | [071 DSCROLL](071_dscroll)               |                    |
| 072    | [072 LSCROLL](072_lscroll)               |                    |
| 073    | [073 CSCROLL](073_cscroll)               |                    |
| 074    | [074 DSCROLLA](074_dscrolla)             |                    |
| 075    | [075 LSCROLLA](075_lscrolla)             |                    |
| 076    | [076 CSCROLLA](076_cscrolla)             |                    |
| 077    | [077 SCROLLSYNC](077_scrollsync)         | Script Processing  |
| 078    | [078 RMOVE](078_rmove)                   |                    |
| 079    | [079 RMOVEA](079_rmovea)                 |                    |
| 07A    | [07A RPMOVEA](07a_rpmovea)               |                    |
| 07B    | [07B RCMOVE](07b_rcmove)                 |                    |
| 07C    | [07C RFMOVE](07c_rfmove)                 |                    |
| 07D    | [07D MOVESYNC](07d_movesync)             | Script Processing  |
| 07E    | [07E CLEAR](07e_clear)                   | Field related      |
| 07F    | [07F DSCROLLP](07f_dscrollp)             |                    |
| 080    | [080 LSCROLLP](080_lscrollp)             |                    |
| 081    | [081 CSCROLLP](081_cscrollp)             |                    |
| 082    | [082 LTURNR](082_lturnr)                 |                    |
| 083    | [083 LTURNL](083_lturnl)                 |                    |
| 084    | [084 CTURNR](084_cturnr)                 |                    |
| 085    | [085 CTURNL](085_cturnl)                 |                    |
| 086    | [086 ADDPARTY](086_addparty)             | Party Management   |
| 087    | [087 SUBPARTY](087_subparty)             | Party Management   |
| 088    | [088 CHANGEPARTY](088_changeparty)       | Party Management   |
| 089    | [089 REFRESHPARTY](089_refreshparty)     | Party Management   |
| 08A    | [08A SETPARTY](08a_setparty)             | Party Management   |
| 08B    | [08B ISPARTY](08b_isparty)               | Party Management   |
| 08C    | [08C ADDMEMBER](08c_addmember)           | Party Management   |
| 08D    | [08D SUBMEMBER](08d_submember)           | Party Management   |
| 08E    | [08E ISMEMBER](08e_ismember)             | Party Management   |
| 08F    | [08F LTURN](08f_lturn)                   |                    |
| 090    | [090 CTURN](090_cturn)                   |                    |
| 091    | [091 PLTURN](091_plturn)                 |                    |
| 092    | [092 PCTURN](092_pcturn)                 |                    |
| 093    | [093 JOIN](093_join)                     | Entity             |
| 094    | [094 MESFORCUS](094_mesforcus)           |                    |
| 095    | [095 BGANIME](095_bganime)               | Field related      |
| 096    | [096 RBGANIME](096_rbganime)             | Field related      |
| 097    | [097 RBGANIMELOOP](097_rbganimeloop)     | Field related      |
| 098    | [098 BGANIMESYNC](098_bganimesync)       | Field related      |
| 099    | [099 BGDRAW](099_bgdraw)                 | Field related      |
| 09A    | [09A BGOFF](09a_bgoff)                   | Field related      |
| 09B    | [09B BGANIMESPEED](09b_bganimespeed)     | Field related      |
| 09C    | [09C SETTIMER](09c_settimer)             | Timer              |
| 09D    | [09D DISPTIMER](09d_disptimer)           | Timer              |
| 09E    | [09E SHADETIMER](09e_shadetimer)         |                    |
| 09F    | [09F SETGETA](09f_setgeta)               |                    |
| 0A0    | [0A0 SETROOTTRANS](0a0_setroottrans)     |                    |
| 0A1    | [0A1 SETVIBRATE](0a1_setvibrate)         |                    |
| 0A2    | [0A2 STOPVIBRATE](0a2_stopvibrate)       |                    |
| 0A3    | [0A3 MOVIEREADY](0a3_movieready)         | Movie              |
| 0A4    | [0A4 GETTIMER](0a4_gettimer)             | Timer              |
| 0A5    | [0A5 FADEIN](0a5_fadein)                 | Field related      |
| 0A6    | [0A6 FADEOUT](0a6_fadeout)               | Field related      |
| 0A7    | [0A7 FADESYNC](0a7_fadesync)             | Script Processing  |
| 0A8    | [0A8 SHAKE](0a8_shake)                   | Field related      |
| 0A9    | [0A9 SHAKEOFF](0a9_shakeoff)             | Field related      |
| 0AA    | [0AA FADEBLACK](0aa_fadeblack)           | Field related      |
| 0AB    | [0AB FOLLOWOFF](0ab_followoff)           |                    |
| 0AC    | [0AC FOLLOWON](0ac_followon)             |                    |
| 0AD    | [0AD GAMEOVER](0ad_gameover)             | Field related      |
| 0AE    | [0AE ENDING](0ae_ending)                 |                    |
| 0AF    | [0AF SHADELEVEL](0af_shadelevel)         |                    |
| 0B0    | [0B0 SHADEFORM](0b0_shadeform)           |                    |
| 0B1    | [0B1 FMOVEA](0b1_fmovea)                 |                    |
| 0B2    | [0B2 FMOVEP](0b2_fmovep)                 |                    |
| 0B3    | [0B3 SHADESET](0b3_shadeset)             |                    |
| 0B4    | [0B4 MUSICCHANGE](0b4_musicchange)       | Music and Sound    |
| 0B5    | [0B5 MUSICLOAD](0b5_musicload)           | Music and Sound    |
| 0B6    | [0B6 FADENONE](0b6_fadenone)             |                    |
| 0B7    | [0B7 POLYCOLOR](0b7_polycolor)           |                    |
| 0B8    | [0B8 POLYCOLORALL](0b8_polycolorall)     |                    |
| 0B9    | [0B9 KILLTIMER](0b9_killtimer)           | Timer              |
| 0BA    | [0BA CROSSMUSIC](0ba_crossmusic)         |                    |
| 0BB    | [0BB DUALMUSIC](0bb_dualmusic)           |                    |
| 0BC    | [0BC EFFECTPLAY](0bc_effectplay)         | Music and Sound    |
| 0BD    | [0BD EFFECTLOAD](0bd_effectload)         | Music and Sound    |
| 0BE    | [0BE LOADSYNC](0be_loadsync)             |                    |
| 0BF    | [0BF MUSICSTOP](0bf_musicstop)           | Music and Sound    |
| 0C0    | [0C0 MUSICVOL](0c0_musicvol)             | Music and Sound    |
| 0C1    | [0C1 MUSICVOLTRANS](0c1_musicvoltrans)   | Music and Sound    |
| 0C2    | [0C2 MUSICVOLFADE](0c2_musicvolfade)     | Music and Sound    |
| 0C3    | [0C3 ALLSEVOL](0c3_allsevol)             | Music and Sound    |
| 0C4    | [0C4 ALLSEVOLTRANS](0c4_allsevoltrans)   | Music and Sound    |
| 0C5    | [0C5 ALLSEPOS](0c5_allsepos)             | Music and Sound    |
| 0C6    | [0C6 ALLSEPOSTRANS](0c6_allsepostrans)   | Music and Sound    |
| 0C7    | [0C7 SEVOL](0c7_sevol)                   | Music and Sound    |
| 0C8    | [0C8 SEVOLTRANS](0c8_sevoltrans)         | Music and Sound    |
| 0C9    | [0C9 SEPOS](0c9_sepos)                   | Music and Sound    |
| 0CA    | [0CA SEPOSTRANS](0ca_sepostrans)         | Music and Sound    |
| 0CB    | [0CB SETBATTLEMUSIC](0cb_setbattlemusic) | Music and Sound    |
| 0CC    | [0CC BATTLEMODE](0cc_battlemode)         | Battle             |
| 0CD    | [0CD SESTOP](0cd_sestop)                 | Music and Sound    |
| 0CE    | [0CE BGANIMEFLAG](0ce_bganimeflag)       |                    |
| 0CF    | [0CF INITSOUND](0cf_initsound)           |                    |
| 0D0    | [0D0 BGSHADE](0d0_bgshade)               |                    |
| 0D1    | [0D1 BGSHADESTOP](0d1_bgshadestop)       |                    |
| 0D2    | [0D2 RBGSHADELOOP](0d2_rbgshadeloop)     |                    |
| 0D3    | [0D3 DSCROLL2](0d3_dscroll2)             |                    |
| 0D4    | [0D4 LSCROLL2](0d4_lscroll2)             |                    |
| 0D5    | [0D5 CSCROLL2](0d5_cscroll2)             |                    |
| 0D6    | [0D6 DSCROLLA2](0d6_dscrolla2)           |                    |
| 0D7    | [0D7 LSCROLLA2](0d7_lscrolla2)           |                    |
| 0D8    | [0D8 CSCROLLA2](0d8_cscrolla2)           |                    |
| 0D9    | [0D9 DSCROLLP2](0d9_dscrollp2)           |                    |
| 0DA    | [0DA LSCROLLP2](0da_lscrollp2)           |                    |
| 0DB    | [0DB CSCROLLP2](0db_cscrollp2)           |                    |
| 0DC    | [0DC SCROLLSYNC2](0dc_scrollsync2)       |                    |
| 0DD    | [0DD SCROLLMODE2](0dd_scrollmode2)       |                    |
| 0DE    | [0DE MENUENABLE](0de_menuenable)         | Menus              |
| 0DF    | [0DF MENUDISABLE](0df_menudisable)       | Menus              |
| 0E0    | [0E0 FOOTSTEPON](0e0_footstepon)         |                    |
| 0E1    | [0E1 FOOTSTEPOFF](0e1_footstepoff)       |                    |
| 0E2    | [0E2 FOOTSTEPOFFALL](0e2_footstepoffall) |                    |
| 0E3    | [0E3 FOOTSTEPCUT](0e3_footstepcut)       |                    |
| 0E4    | [0E4 PREMAPJUMP](0e4_premapjump)         |                    |
| 0E5    | [0E5 USE](0e5_use)                       | Entity             |
| 0E6    | [0E6 SPLIT](0e6_split)                   | Entity             |
| 0E7    | [0E7 ANIMESPEED](0e7_animespeed)         | Animation          |
| 0E8    | [0E8 RND](0e8_rnd)                       |                    |
| 0E9    | [0E9 DCOLADD](0e9_dcoladd)               |                    |
| 0EA    | [0EA DCOLSUB](0ea_dcolsub)               |                    |
| 0EB    | [0EB TCOLADD](0eb_tcoladd)               |                    |
| 0EC    | [0EC TCOLSUB](0ec_tcolsub)               |                    |
| 0ED    | [0ED FCOLADD](0ed_fcoladd)               | Field related      |
| 0EE    | [0EE FCOLSUB](0ee_fcolsub)               | Field related      |
| 0EF    | [0EF COLSYNC](0ef_colsync)               | Script processing  |
| 0F0    | [0F0 DOFFSET](0f0_doffset)               |                    |
| 0F1    | [0F1 LOFFSETS](0f1_loffsets)             |                    |
| 0F2    | [0F2 COFFSETS](0f2_coffsets)             |                    |
| 0F3    | [0F3 LOFFSET](0f3_loffset)               |                    |
| 0F4    | [0F4 COFFSET](0f4_coffset)               |                    |
| 0F5    | [0F5 OFFSETSYNC](0f5_offsetsync)         |                    |
| 0F6    | [0F6 RUNENABLE](0f6_runenable)           | Entity             |
| 0F7    | [0F7 RUNDISABLE](0f7_rundisable)         | Entity             |
| 0F8    | [0F8 MAPFADEOFF](0f8_mapfadeoff)         | Field related      |
| 0F9    | [0F9 MAPFADEON](0f9_mapfadeon)           | Field related      |
| 0FA    | [0FA INITTRACE](0fa_inittrace)           |                    |
| 0FB    | [0FB SETDRESS](0fb_setdress)             | Entity             |
| 0FC    | [0FC GETDRESS](0fc_getdress)             | Entity             |
| 0FD    | [0FD FACEDIR](0fd_facedir)               | Entity             |
| 0FE    | [0FE FACEDIRA](0fe_facedira)             |                    |
| 0FF    | [0FF FACEDIRP](0ff_facedirp)             |                    |
| 100    | [100 FACEDIRLIMIT](100_facedirlimit)     |                    |
| 101    | [101 FACEDIROFF](101_facediroff)         |                    |
| 102    | [102 SARALYOFF](102_saralyoff)           |                    |
| 103    | [103 SARALYON](103_saralyon)             |                    |
| 104    | [104 SARALYDISPOFF](104_saralydispoff)   |                    |
| 105    | [105 SARALYDISPON](105_saralydispon)     |                    |
| 106    | [106 MESMODE](106_mesmode)               | Message            |
| 107    | [107 FACEDIRINIT](107_facedirinit)       |                    |
| 108    | [108 FACEDIRI](108_facediri)             |                    |
| 109    | [109 JUNCTION](109_junction)             | Party Management   |
| 10A    | [10A SETCAMERA](10a_setcamera)           | Field related      |
| 10B    | [10B BATTLECUT](10b_battlecut)           |                    |
| 10C    | [10C FOOTSTEPCOPY](10c_footstepcopy)     |                    |
| 10D    | [10D WORLDMAPJUMP](10d_worldmapjump)     | Field related      |
| 10E    | [10E RFACEDIRI](10e_rfacediri)           |                    |
| 10F    | [10F RFACEDIR](10f_rfacedir)             |                    |
| 110    | [110 RFACEDIRA](110_rfacedira)           |                    |
| 111    | [111 RFACEDIRP](111_rfacedirp)           |                    |
| 112    | [112 RFACEDIROFF](112_rfacediroff)       |                    |
| 113    | [113 FACEDIRSYNC](113_facedirsync)       |                    |
| 114    | [114 COPYINFO](114_copyinfo)             |                    |
| 115    | [115 PCOPYINFO](115_pcopyinfo)           |                    |
| 116    | [116 RAMESW](116_ramesw)                 | Message            |
| 117    | [117 BGSHADEOFF](117_bgshadeoff)         | Field related      |
| 118    | [118 AXIS](118_axis)                     |                    |
| 119    | [119 AXISSYNC](119_axissync)             |                    |
| 11A    | [11A MENUNORMAL](11a_menunormal)         | Menus              |
| 11B    | [11B MENUPHS](11b_menuphs)               | Menus              |
| 11C    | [11C BGCLEAR](11c_bgclear)               |                    |
| 11D    | [11D GETPARTY](11d_getparty)             | Party Management   |
| 11E    | [11E MENUSHOP](11e_menushop)             | Menus              |
| 11F    | [11F DISC](11f_disc)                     | Field related      |
| 120    | [120 DSCROLL3](120_dscroll3)             |                    |
| 121    | [121 LSCROLL3](121_lscroll3)             |                    |
| 122    | [122 CSCROLL3](122_cscroll3)             |                    |
| 123    | [123 MACCEL](123_maccel)                 |                    |
| 124    | [124 MLIMIT](124_mlimit)                 |                    |
| 125    | [125 ADDITEM](125_additem)               | Item/Magic/Card/GF |
| 126    | [126 SETWITCH](126_setwitch)             |                    |
| 127    | [127 SETODIN](127_setodin)               |                    |
| 128    | [128 RESETGF](128_resetgf)               |                    |
| 129    | [129 MENUNAME](129_menuname)             | Menus              |
| 12A    | [12A REST](12a_rest)                     |                    |
| 12B    | [12B MOVECANCEL](12b_movecancel)         |                    |
| 12C    | [12C PMOVECANCEL](12c_pmovecancel)       |                    |
| 12D    | [12D ACTORMODE](12d_actormode)           |                    |
| 12E    | [12E MENUSAVE](12e_menusave)             | Menus              |
| 12F    | [12F SAVEENABLE](12f_saveenable)         | Menus              |
| 130    | [130 PHSENABLE](130_phsenable)           | Menus              |
| 131    | [131 HOLD](131_hold)                     | Party Management   |
| 132    | [132 MOVIECUT](132_moviecut)             |                    |
| 133    | [133 SETPLACE](133_setplace)             |                    |
| 134    | [134 SETDCAMERA](134_setdcamera)         |                    |
| 135    | [135 CHOICEMUSIC](135_choicemusic)       |                    |
| 136    | [136 GETCARD](136_getcard)               |                    |
| 137    | [137 DRAWPOINT](137_drawpoint)           | Menus              |
| 138    | [138 PHSPOWER](138_phspower)             |                    |
| 139    | [139 KEY](139_key)                       |                    |
| 13A    | [13A CARDGAME](13a_cardgame)             | Menus              |
| 13B    | [13B SETBAR](13b_setbar)                 |                    |
| 13C    | [13C DISPBAR](13c_dispbar)               |                    |
| 13D    | [13D KILLBAR](13d_killbar)               |                    |
| 13E    | [13E SCROLLRATIO2](13e_scrollratio2)     |                    |
| 13F    | [13F WHOAMI](13f_whoami)                 |                    |
| 140    | [140 MUSICSTATUS](140_musicstatus)       |                    |
| 141    | [141 MUSICREPLAY](141_musicreplay)       |                    |
| 142    | [142 DOORLINEOFF](142_doorlineoff)       | Entity             |
| 143    | [143 DOORLINEON](143_doorlineon)         | Entity             |
| 144    | [144 MUSICSKIP](144_musicskip)           |                    |
| 145    | [145 DYING](145_dying)                   | Party Management   |
| 146    | [146 SETHP](146_sethp)                   | Party Management   |
| 147    | [147 GETHP](147_gethp)                   | Party Management   |
| 148    | [148 MOVEFLUSH](148_moveflush)           |                    |
| 149    | [149 MUSICVOLSYNC](149_musicvolsync)     |                    |
| 14A    | [14A PUSHANIME](14a_pushanime)           |                    |
| 14B    | [14B POPANIME](14b_popanime)             |                    |
| 14C    | [14C KEYSCAN2](14c_keyscan2)             | Input              |
| 14D    | [14D KEYON2](14d_keyon2)                 | Input              |
| 14E    | [14E PARTICLEON](14e_particleon)         |                    |
| 14F    | [14F PARTICLEOFF](14f_particleoff)       |                    |
| 150    | [150 KEYSIGHNCHANGE](150_keysighnchange) |                    |
| 151    | [151 ADDGIL](151_addgil)                 | Item/Magic/Card/GF |
| 152    | [152 ADDPASTGIL](152_addpastgil)         | Item/Magic/Card/GF |
| 153    | [153 ADDSEEDLEVEL](153_addseedlevel)     | Item/Magic/Card/GF |
| 154    | [154 PARTICLESET](154_particleset)       |                    |
| 155    | [155 SETDRAWPOINT](155_setdrawpoint)     |                    |
| 156    | [156 MENUTIPS](156_menutips)             | Menus              |
| 157    | [157 LASTIN](157_lastin)                 |                    |
| 158    | [158 LASTOUT](158_lastout)               |                    |
| 159    | [159 SEALEDOFF](159_sealedoff)           |                    |
| 15A    | [15A MENUTUTO](15a_menututo)             | Menus              |
| 15B    | [15B OPENEYES](15b_openeyes)             |                    |
| 15C    | [15C CLOSEEYES](15c_closeeyes)           |                    |
| 15D    | [15D BLINKEYES](15d_blinkeyes)           |                    |
| 15E    | [15E SETCARD](15e_setcard)               | Item/Magic/Card/GF |
| 15F    | [15F HOWMANYCARD](15f_howmanycard)       | Item/Magic/Card/GF |
| 160    | [160 WHERECARD](160_wherecard)           | Item/Magic/Card/GF |
| 161    | [161 ADDMAGIC](161_addmagic)             | Item/Magic/Card/GF |
| 162    | [162 SWAP](162_swap)                     |                    |
| 163    | [163 SETPARTY2](163_setparty2)           |                    |
| 164    | [164 SPUSYNC](164_spusync)               | Timer              |
| 165    | [165 BROKEN](165_broken)                 |                    |
| 166    | [166 UNKNOWN1](166_unknown1)             |                    |
| 167    | [167 UNKNOWN2](167_unknown2)             |                    |
| 168    | [168 UNKNOWN3](168_unknown3)             |                    |
| 169    | [169 UNKNOWN4](169_unknown4)             |                    |
| 170    | [170 UNKNOWN5](170_unknown5)             | Item/Magic/Card/GF |
| 171    | [171 UNKNOWN6](171_unknown6)             | Animation          |
| 172    | [172 UNKNOWN7](172_unknown7)             | Animation          |
| 173    | [173 UNKNOWN8](173_unknown8)             | Animation          |
| 174    | [174 UNKNOWN9](174_unknown9)             | Animation          |
| 175    | [175 UNKNOWN10](175_unknown10)           |                    |
| 176    | [176 UNKNOWN11](176_unknown11)           |                    |
| 177    | [177 UNKNOWN12](177_unknown12)           |                    |
| 178    | [178 UNKNOWN13](178_unknown13)           | Music and Sound    |
| 179    | [179 UNKNOWN14](179_unknown14)           | Music and Sound    |
| 180    | [180 UNKNOWN15](180_unknown15)           |                    |
| 181    | [181 UNKNOWN16](181_unknown16)           | Field related      |
| 182    | [182 UNKNOWN17](182_unknown17)           | Field related      |
| 183    | [183 UNKNOWN18](183_unknown18)           | Menus              |