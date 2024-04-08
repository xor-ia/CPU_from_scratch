import sys
from utils import disp


def regToInt(r:str):
    if r == "ram":
        return 15
    if r == "pc":
        return 16
    if r == "sp":
        return 32
    
    return int(r[1:])




def assemble(src, v1Mode=False):
    src = src.lower()
    if v1Mode:
        conditionLookup = {k:v for v, k in enumerate(["true", "false", "=0", "!0", ">0", "<0", ">=0", "<=0"])}
    else:
       conditionLookup = {k:v for v, k in enumerate(["false", "=0", "<0", "<=0", "true", "!0", ">=0", ">0"])}
     
    operationLookup = {k:v for v, k in enumerate(["and", "or", "xor", "not", "add", "sub", "mul", "div", "ls", "rs"])}
    result = []
    lineno = 0
    for i in src.split("\n"):
        if i == "" or i.startswith(";"):
            continue
        i = i.split(";")[0].replace("\t", " ").split(" ")
        currLine = 0
        cmd = i[0]
        if cmd == "inst":
            v = int(i[1])
            if v > 4095:
                disp("SRC - {} : instantiating a number larger than 12 bit.", lineno+1, level=1)
            v = v & 4095 # clip to be 12 bit
            currLine |= int(i[1])
        elif cmd == "move":
            currLine |= (1 << 12) | (regToInt(i[1]) << 6) | regToInt(i[2])
        elif cmd == "calc":
            currLine |= (2 << 12) | (operationLookup[i[1]] << 6) | regToInt(i[2])
        elif cmd == "jumpif":
            a0 = 0
            a1 = 0
            if i[1] in ["true", "false"]:
                a1 = conditionLookup[i[1]]
            else:
                a0 = regToInt(i[1])
                a1 = conditionLookup[i[2]]
            currLine |= (3 << 12) | (a0 << 6) | a1

        elif cmd == "push":
            currLine |= (4 << 12) | (regToInt(i[1]) << 6)
        elif cmd == "pop":
            currLine |= (5 << 12) | regToInt(i[1])
        elif cmd == "halt":
            currLine = (1<<16)-1
        else:
            disp("Unknown keyword \"{}\"", cmd, level=2)
        result.append(currLine)
        lineno += 1

    return " ".join([f"{i:04x}" for i in result])



if __name__ != "__main__":
    exit(0)


if len(sys.argv) == 1:
    disp("No source file provided!", level=2)

try:
    src = open(sys.argv[1], "r").read()
except FileNotFoundError:
    disp("No such file named \"{}\".", sys.argv[1], level=2)
except PermissionError:
    disp("Cannot read file \"{}\". Permission denied.", sys.argv[1], level=2)

print(assemble(src))