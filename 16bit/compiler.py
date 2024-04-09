import sys
from utils import disp

if __name__ != "__main__":
    exit(0)

ptrTo = "PTR_TO_"
valueOf = "VALUE_OF_"
WP = "WAYPOINT_"


if len(sys.argv) == 1:
    disp("No source file provided!", level=2)

try:
    src = open(sys.argv[1], "r").read()
except FileNotFoundError:
    disp("No such file named \"{}\".", sys.argv[1], level=2)
except PermissionError:
    disp("Cannot read file \"{}\". Permission denied.", sys.argv[1], level=2)

def intHelp(v):
    # help load int16 to r0
    if v < 4096:
        return f"inst {v}\n"
    if v > 65535:
        disp("Overflow : 0 <=! {} <=! 65535", v, level=2)
    instruct += f"push r1\n"
    instruct += f"push r2\n"
    
    instruct += f"inst {v // 16}\n"
    instruct += f"move r0 r1\n"
    instruct += f"inst 4\n"
    instruct += f"move r0 r2\n"
    instruct += f"calc ls r1\n"
    instruct += f"inst {v % 16}\n"
    instruct += f"move r0 r2\n"
    instruct += f"calc or r0\n"

    instruct += f"pop r1\n"
    instruct += f"pop r2\n"
    
    return instruct

def varQuery(ptr):
    instruct = intHelp(ptr) # pointer to variable
    instruct += "move r0 r3\n" # load pointer
    instruct += "move ram r0\n" # load value
    return instruct
    

def numberHelper(n:str):
    if n.startswith("0x"):
        return int(n[2:],16)
    if n.startswith("0b"):
        return int(n[2:],2)
    if n.isnumeric():
        return int(n)
    return None

def expHelp(expression):
    # expression helper
    # generate command to evaluate expression and store result to r0

    if len(expression) == 1:
        n = numberHelper(expression[0])
        if n != None:
            return intHelp(n) # this is a number
        else: #probably a variable
            varname = expression[0]
            instr = ""
            instr += f"{valueOf}{varname}\n"
            return instr
    
    instr = ""
    opmap = {
        "+": "add",
        "-": "sub",
        "*": "mul",
        "/": "div",
        "<<": "ls",
        ">>": "rs",
        "&": "and",
        "|": "or",
        "^": "xor",
    }
    # load first arg and second
    # load 1
    instr += f"push r1\n"
    instr += f"push r2\n"
    
    instr += f"{valueOf}{expression[0]}\n"
    instr += f"move r0 r1\n"
    
    for i in range(1, len(expression), 2):
        operator = expression[i]
        arg = expression[i+1]
        instr += f"push r1\n"
        instr += f"{valueOf}{arg}\n"
        instr += f"pop r1\n"
        instr += f"move r0 r2\n"
        instr += f"calc {opmap[operator]} r1\n"

    instr += f"move r1 r0\n"

    instr += f"pop r1\n"
    instr += f"pop r2\n"
    
    return instr
        
        # probably a variable

# parsing
parsed = list(filter(lambda x: x!="" and not x.startswith(";"), src.split("\n")))
parsed = [" ".join(filter(lambda x: x!="", i.split(";")[0].split(" "))) for i in parsed] # removing comment and whiteSpace


varMap = {}
varN = 0

# determine amount of memory needed
for n, line in enumerate(parsed):
    if line.startswith("let"):
        varname = line.split(" ")[1]
        if not varname in varMap.keys():
            varMap[varname] = varN
            varN += 1
            


curr_exec = "; initializing bp\n"
curr_exec += "move sp bp\n"
curr_exec += "; allocating some space for variables\n"
curr_exec += "move sp r1\n"
curr_exec += intHelp(varN)
curr_exec += "move r0 r2\n"
curr_exec += "calc sub sp\n"
curr_exec += "; bp now point to bottom of the stackframe\n\n"


# actually compiling
for n, line in enumerate(parsed):
    if line.startswith(":"):
        curr_exec += f"{WP}{line[1:]}\n\n"
        continue # skip. this is not instruction just a waypoint
    tokens = line.split(" ")
    cmd = tokens[0]
    curr_exec += f"; {line}\n"
    if line.startswith("let"):
        varname = tokens[1]
        
        curr_exec += "; expression begin\n"
        curr_exec += expHelp(tokens[3:])
        curr_exec += "; expression end\n"
        curr_exec += f"push r0\n" # ; temporarily save the value while loading destination address
        curr_exec += f"{ptrTo}{varname}\n"
        curr_exec += f"move r0 r3\n"
        curr_exec += f"pop r0\n" # ; retrieve value to move to ram
        curr_exec += f"move r0 ram\n"
    elif line.startswith("goto"):
        curr_exec += line 

    curr_exec += "\n\n"

new_exec = []
for line in curr_exec.split("\n"):
    if line.startswith(ptrTo) and line[len(ptrTo):] in varMap.keys():
        offset = varMap[line[len(ptrTo):]]
        instruct = "; auto ptrTo\nmove bp r1\n"
        instruct = instruct + intHelp(offset)
        instruct = instruct + "move r0 r2\ncalc sub r0\n\n"
        new_exec = new_exec + instruct.split("\n")
    elif line.startswith(valueOf) and line[len(valueOf):] in varMap.keys():
        offset = varMap[line[len(valueOf):]]
        instruct  = "; auto valueOf\nmove bp r1\n"
        instruct += intHelp(offset)
        instruct += "move r0 r2\ncalc sub r3\nmove ram r0\n\n"
        new_exec = new_exec + instruct.split("\n")
    else:
        new_exec.append(line)


curr_exec = "\n".join(new_exec) + "halt\n"
new_exec = []
# handling goto states
for line in curr_exec.split("\n"):
    if line.startswith("goto"):
        args = line.split(" ")
        waypointName = args[2]
        conditioned = len(args) > 3
    else:
        new_exec.append(line)
curr_exec = "\n".join(new_exec) + "halt\n"


outpath = "a.out" if len(sys.argv) == 2 else sys.argv[3]
disp("Storing result to {}", outpath)
open(outpath, "w").write(curr_exec)