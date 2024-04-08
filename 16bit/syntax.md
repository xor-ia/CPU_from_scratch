# Keywords

```
let    : declare variable
goto   : goto   // can stack if statement
set    : set ram to value
push   : push stack
pop    : pop stack
```
# Datatypes

```
Only int exist. I'm lazy :3

0x prefix denotes hex value.
0b prefix denotes binary value.

```


# Variable declaration

`let varname = value`

# Operations

```
let a = 420
let b = 69
let result = $a + $b
```
**Math operation has no parentheses and will always execute from left to right**
- & : and
- | : or
- ^ : xor
- ! : not
- \+ : add
- \- : sub
- \* : mul
- / : div
- << : left shift
- \>> : right shift
 


# Goto

```
let a = 0
let b = 1

:waypoint
let a = a + b

goto :skip if a > 128
goto :waypoint

:skip

set 0x0030 $a
```

# Example compiled code
## this is not true. im just stupid

`let a = 0`
```
inst 0  ; is in r0
push r0 ; &a is 0xFFFF
```
`let b = 1`
```
inst 1  ; is in r0
push r0 ; &b is 0xFFFE (compiler knows cuz it just count lmao)
```
`let ptr_a = &a`
```
; since address of a is 0xFFFF but we can only initialize 0xFFF at a time it will do a pro gamer move
inst 4095  ; is in r0
move r0 r1 ;
inst 4          
move r0 r2 ; r1 is 0xFFF, r2 is 1
calc ls r1 ; shift r1 by 4 bit and store it back to r1
inst 15    ; 0x000F
move r0 r2 ; r1 is 0xFFF0, r2 is 0x000F
calc or r0 ; r0 now store 0xFFFF which is $a address
push r0    ; 0xFFFD now contains 0xFFFF
; and we can just remember that 0xFFFD is ptr_a's address
```