---
layout: default
title: Field Opcodes
parent: Field
nav_order: 2
author: Aali, myst6re, Shard
permalink: /technical-reference/field/field-opcodes/
---

## The language

The field script language in ff8 is a simple assembly language with a stack. Here is an example:

```
stack =  []

PSHM_W   1024 # push  var1024  onto  the  stack  (stack =  [var1024])  
PSHN_L   6 # push  number  6  onto  the  stack  (stack =  [6Â ; var1024])  
CAL      EQ # compare  the  two  numbers  at  the  top  of  the  stack, pop  this  numbers, and  push  the  result  (1  or  0)  into  the  stack  (stack =  [1  or  0])    
JPF      LABEL1 # if  the  popped  top  of  the  stack  is  0, jump  to  LABEL1  (stack =  [])  
PSHN_L   0 # push  0  at  the  top  of  the  stack  (stack =  [0])  
POPM_W   1024 # pop  the  top  of  the  stack  into  var1024  (stack =  [])  
JMP      LABEL2 # goto  LABEL2  
LABEL1          
PSHN_L   1 # push  1  at  the  top  of  the  stack  (stack =  [1])  
POPM_W   1024 # pop  the  top  of  the  stack  into  var1024  (stack =  [])  
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
listed separately, if the function requires one. For example, on the page for [SET3](01E-set3), the parameters are listed like this:

*XCoord*

*YCoord*

*ZCoord*

**SET3**

Which means when you call **SET3**, the ZCoord is the top item on the stack, YCoord is under it, and XCoord is under that, for example

```
PSHN_L  402   (XCoord)
PSHN_L  -381  (YCoord)  
PSHN_L  20    (ZCoord)  
SET3    17    (walkmesh  triangle  ID)
```
