
def filt(l, f):
    return list(filter(f, l))

def pattern_match(template, data):
    valid = True
    for i in range(len(data)):
        if template[i] == "x":
            continue
        valid = valid and data[i] == template[i]
    return valid



src = list(map(
    lambda x: filt(
        x.split(" "), 
        lambda x : len(x) != 0
    ),
    filt(
        open("instr.txt", "r").read().split("\n"), 
        lambda x : len(x) != 0
    )
))



rules = {}

# {high bit -> {low bit -> {rules -> instr}}}

for i in src:
    h, m, l = i[0], i[1], f"{int(i[2])+2:04b}"
    if h not in rules:
        rules[h] = {}
    if l not in rules[h]:
        rules[h][l] = {}
    rules[h][l][m] = i[4:]
    

word2int = {
    v : 1<<i for i,v in enumerate(['RAI', 'RAO', 'RBI', 'RBO', 'MAI', 'RMI', 'RMO', 'ALO', 'AFO', 'SUB', 'PCI', 'PCO', 'PCC', 'II', 'IO', 'SPI', 'SPO', 'SPC', 'SPQ', 'BPI', 'BPO', 'OO', 'EI', 'HLT'])}
result = ""

for i in range(2**12):
    binrep = f"{i:012b}"
    h, m, l = (binrep[i: i+4] for i in range(0, 12, 4))
    totalmicro = []
    if l == "0000":
        totalmicro = ["PCO", "MAI"]
    elif l == "0001":
        totalmicro = ["RMO", "II", "PCC"]
    elif h in rules:
        if l in rules[h]:
            for rule, mcc in rules[h][l].items():
                if pattern_match(rule, m):
                    totalmicro += mcc

    n = 0
    for word in totalmicro:
        n = n | word2int[word]
    print(h, m, l, totalmicro, f"{n:06x}")
    result += f"{n:06x} "
    

open("instr_rom.txt", "w").write(result)

    