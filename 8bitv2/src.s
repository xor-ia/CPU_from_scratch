
// this program calculate fib sequence


IB 1
PUSH A
POP A
PUSH B 
ADD B
POP A 
OUT B

PUSH A 
IA 15
MOV A BP
POP A
JMPO BP

PUSH A 
IA 2
JMP A 
HALT