#!/bin/bash

# Make backup
cp level2 level2.backup 

# we have 3 diffrent checkpoin at this program that we will make to check the input itselfe first is to eliminate the indexes taht must = 0 
# then we make comparison at the string made to itself 
r2 -w -e bin.relocs.apply=true level2 <<EOF
s 0x00001335
wa cmp eax, eax 
s 0x0000134e
wa cmp eax, eax
wx 39c090 @ 0x0000146a
q
EOF

