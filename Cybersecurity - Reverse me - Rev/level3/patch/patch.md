# level3 patch

just in the folder contain level3 run :
```bash
chmod +x patch.sh &&  ./patch.sh
```

### step by step: 

the first 2 indexes check .

```bash 
[0x0000136e]> s 0x0000000000001365
[0x00001365]> pd 8
            0x00001365      0fbe4dc1       movsx ecx, byte [rbp - 0x3f]
            0x00001369      b832000000     mov eax, 0x32               ; '2'
            0x0000136e      39c8           cmp eax, ecx                 # NOP out this 
        ┌─< 0x00001370      0f8405000000   je 0x137b
        │   0x00001376      e865ffffff     call sym.___syscall_malloc
        └─> 0x0000137b      0fbe4dc0       movsx ecx, byte [rbp - 0x40]
            0x0000137f      b834000000     mov eax, 0x34               ; '4'
            0x00001384      39c8           cmp eax, ecx                # NOP out this
[0x00001365]> wx 9090 @ 0x0000136e
[0x00001365]> wx 9090 @ 0x00001384
[0x00001365]> pd 8
```

the final cmp after atoi call an strcmp force to return 0.

```bash
[0x00001438]> s 0x00001475
[0x00001475]> pd 6
            0x00001475      e8f6fbffff     call sym.imp.strcmp
            0x0000147a      8945f0         mov dword [rbp - 0x10], eax
            0x0000147d      8b45f0         mov eax, dword [rbp - 0x10]
            0x00001480      8945ac         mov dword [rbp - 0x54], eax
            0x00001483      83e8fe         sub eax, 0xfffffffe
        ┌─< 0x00001486      0f84aa000000   je 0x1536
```
it is a 5 byte so we write a 2 byte xor eax, eax and NOP out the rest 3 bytes.
```bash
[0x00001475]> wa xor eax, eaxoptinon1
INFO: Written 2 byte(s) (xor eax, eax) = wx 31c0 @ 0x00001475
[0x00001475]> pd 6
            0x00001475      31c0           xor eax, eax
            0x00001477      fb             sti
            0x00001478      ff             invalid
            0x00001479      ff8945f08b45   dec dword [rcx + 0x458bf045]
            0x0000147f      f0             invalid
            0x00001480      8945ac         mov dword [rbp - 0x54], eax
[0x00001475]> wx 90 @ 0x00001477
[0x00001475]> pd 6
            0x00001475      31c0           xor eax, eax
            0x00001477      90             nop
            0x00001478      ff             invalid
            0x00001479      ff8945f08b45   dec dword [rcx + 0x458bf045]
            0x0000147f      f0             invalid
            0x00001480      8945ac         mov dword [rbp - 0x54], eax
[0x00001475]> wx 9090 @ 0x00001478
[0x00001475]> pd 6
            0x00001475      31c0           xor eax, eax
            0x00001477      90             nop
            0x00001478      90             nop
            0x00001479      90             nop
            0x0000147a      8945f0         mov dword [rbp - 0x10], eax
            0x0000147d      8b45f0         mov eax, dword [rbp - 0x10]
[0x00001475]> q
```
or 

```bash
[0x00001438]> wx 31c0909090 @ 0x00001475
```
