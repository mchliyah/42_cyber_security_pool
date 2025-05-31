#!/bin/bash

# Make backup
cp level1 level1.backup

# Apply patch using direct byte writing , making the strcmp compair the input to itself
# at the 0x00001232 the program load the hardcoded check string we will replace it with the input next instruction at 0x00001235 so this one is 3 byte 
# avoiding the SEGV sense we will set a two byte instruction we will add a 1 byte padding at  0x00001234
r2 -w -e bin.relocs.apply=true level1 <<EOF
s 0x00001232
wa mov edx, ecx 
s 0x00001234
wa nop
q
EOF

# Verify patch
echo "Verifying patch:"
r2 -e bin.relocs.apply=true -q -c 'pd 5 @ 0x00001230' level1

