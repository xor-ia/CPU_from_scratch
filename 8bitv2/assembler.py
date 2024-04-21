import sys



if __name__ != "__main__":
    exit(0)

argv = sys.argv

assert len(argv) > 1, "where is the src file my man"

src = list(filter(lambda x: len(x) > 0,[i.split("//")[0] for i in filter(lambda x: len(x) > 0, open(argv[1], "r").read().upper().split("\n"))]))
mapping = {
    "IA" : "0000",
    "IB" : "0001",
    "CALC": "0010",
    "MOV": "0011",
    "LOAD": "0100",
    "STORE": "0101",
    "OUT": "0110",
    "PUSH": "0111",
    "POP": "1000",
    "JMP": "1001",
    "JMPZ": "1010",
    "JMPG": "1011",
    "JMPL": "1100",
    "JMPE": "1101",
    "JMPO": "1110",
    "HALT": "1111",
}

REGMAP = {
    "A": "00",
    "B": "01",
    "SP": "10",
    "BP": "11",
}


for i in src:
    isp = i.split(" ")
    instruction = isp[0]
    upperbit = "00"
    lowerbit = "00"
    
    if instruction in ["MOV", "LOAD", "STORE", "OUT", "PUSH", "POP"] or instruction.startswith("JMP"):
        upperbit = REGMAP[isp[1]]
    if instruction in ["MOV", "LOAD", "STORE"]:
        lowerbit = REGMAP[isp[2]]
    if instruction == "ADD":
        upperbit = REGMAP[isp[1]]
        instruction = "CALC"
    if instruction == "SUB":
        upperbit = REGMAP[isp[1]]
        instruction = "CALC"
        lowerbit = "01"
    if instruction in ["IA", "IB"]:
        rep = f"{int(isp[1]):04b}"[:4] # ensure 4 bit
        upperbit = rep[0:2]
        lowerbit = rep[2:4]
    
    hxrep = f"{int(mapping[instruction]+upperbit+lowerbit, 2):02x}"
    print(hxrep, end=" ")