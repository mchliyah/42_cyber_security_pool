#!/bin/bash

# Make backup
cp level3 level3.backup 

r2 -w -e bin.relocs.apply=true level3 <<EOF
wx 9090 @ 0x0000136e
wx 9090 @ 0x00001384
wx 31c0909090 @ 0x00001475
q
EOF
