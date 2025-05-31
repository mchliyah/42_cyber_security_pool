# Binary Patching Explanation

## Original Behavior
The program checks user input against a hardcoded string "__stack_check" using strcmp().

## Patch Applied
1. Located the strcmp vars loading "expected input" at address 0x00001232
2. Replaced the move instruction with `mov edx, ecx` which sets the target string to the user input
3. NOP-filled the remaining bytes of the original call instruction it is one byte here `0x00001234`

## Effect
The patched binary will now accept any password as valid since:
- The comparison is the user_input to itselfe
- The program now proceeds to the "Good job!" branch in all cases 

## How to Apply
Run the patch.sh to automatically apply these changes to the binary.