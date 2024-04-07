import sys

"""
00[data 6bit]             | store to REG0
01[oprand 6 bit]          | calc REG1 to REG2 and store to REG3
   000000 : XOR
   000001 : AND
   000010 : OR
   000011 : NOT
   000100 : ADD
   000101 : SUB
   000110 : MUL
   000111 : DIV
10[from 3 bit][to 3 bit]  | copy data
   000 : REG0
   001 : REG1
   010 : REG2
   011 : REG3
   100 : REG4
   101 : REG5
   110 : REG6
   111 : RAM(Address at REG0)
11[condition 6 bit]       | jump to address in REG0 if REG3 match condition
   000000 : ALWAYS
   000001 : NEVER
   000010 : =0
   000011 : !=0
   000100 : >0
   000101 : <0
   000110 : >=0
   000111 : <=0

asm

inst i6
calc [xor/and/or/not/add/sub/mul/div]
copy [r0-r6/ram]
chck [true/false/z/nz/gtz/ltz/gtez/ltez]

"""


if __name__ != "__main__":
    exit(0)

args = sys.argv
name = args[1]
src = open(name, "r").read().split("\n")

codes = {
    "inst": "00",
    "calc": "01",
    "copy": "10",
    "chck": "11",
    "xor" : "000000",
    "and" : "000001",
    "or"  : "000010",
    "not" : "000011",
    "add" : "000100",
    "sub" : "000101",
    "mul" : "000110",
    "div" : "000111",
    "r0"  : "000",
    "r1"  : "001",
    "r2"  : "010",
    "r3"  : "011",
    "r4"  : "100",
    "r5"  : "101",
    "r6"  : "110",
    "ram" : "111",
    "true": "000000",
    "false": "000001",
    "z"   : "000010",
    "nz"  : "000011",
    "gtz" : "000100",
    "ltz" : "000101",
    "gtez": "000110",
    "ltez": "000111",
}

instructions = []
nd = 0
flags = []
for v in src:
    if v == "" or v.startswith(";"):
        continue

    i = v.split(" ")
    tmp = ""
    tmp += codes[i[0]]
    if i[0] == "inst":
        # this next one will always be data in integer
        d = int(i[1])
        d = f"{d:06b}"
        if len(d) != 6:
            print(f"Assembler warning [Line : {nd+1}] : (inst) binary conversion lenght != 6 ({len(d)}). Discarding...")
            d = d[:6] 
        tmp+=d
    elif i[0] == "calc" or i[0] == "chck":
        tmp += codes[i[1]]
    elif i[0] == "copy":
        tmp += codes[i[1]] + codes[i[2]]
    nd +=1
    instructions.append([tmp, v])

print("Output")
outcpy = ""
for v in instructions:
    i = v[0]
    print(f"BIN[{i}] : HEX[{int(i, 2):02x}] : OG[{v[1]}]")
    outcpy += f"{int(i, 2):02x} "
print("copy")
print(outcpy)









