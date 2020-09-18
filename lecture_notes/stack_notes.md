The CPU Stack
-------------

Why is there a stack in the CPU?

Stack is good for:
* Temporarily storing values
* It also makes subroutines (functions) possible
* Implementing local variables
* It's easy to implement in the CPU hardware.


PUSH:
1. Decrement SP
2. Copy the register value into SP's location

POP:
1. Copy value from SP's location to the reg
2. Incrememnt SP




R0: 12
R1: 4A
R2: 99
R3: 99
...
R7: F3 (this is the SP)

PUSH R0 
PUSH R1
PUSH R2 
PUSH R3 
POP R2 
POP R1 
POP R0 
POP R0 <<