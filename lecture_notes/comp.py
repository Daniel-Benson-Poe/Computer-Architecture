import sys

"""
Get the file path from the command line
Sanitize the data from that file
    Ignore blank lines, whitespace, comments
    Splitting the input file per line
    Turn into program instructions (str->int)
"""

# These all mean the same thing:
#### Index into the memory array
#### Address
#### Location
#### Pointer

## operands == arguments to the instruction

memory = [0] * 256

if len(sys.argv) != 2:
    print("usage: comp.py filename")
    sys.exit(1)

try:
    address = 0

    with open(sys.argv[1]) as f:
        for line in f:
            t = line.split('#')
            n = t[0].strip()

            if n == '':
                continue
            
            try:
                n = int(n)
            except ValueError:
                print(f"Invalid number '{n}'")
                sys.exit()
            
            memory[address] = n
            address += 1

except FileNotFoundError:
    print(f"File not found: {sys.argv[1]}")
    sys.exit(2)


registers = [0] * 8  # R0-R7

# Variables in hardware.. Known as "registers".
# There are a fixed number of registers - we can't make more beyond manufacturing a new chip that has more
# They have fixed names
# R0, R1, R2, ..., R6, R7

pc = 0  # "Program Counter": address of the currently-executing instruction

SP = 7

SAVE_REG = 3
PRINT_REG = 4
PRINT_BEEJ = 1
PUSH = 5
POP = 6
HALT = 2
CALL = 7
RET = 8


registers[SP] = 0xF4  # Init SP

def push_value(v):
    # Decrement SP
        registers[SP] -= 1

        # copy value to SP
        top_of_stack_addr = registers[SP]
        memory[top_of_stack_addr] = v

def pop_value():

        # get top of stack addr
        top_of_stack_addr = registers[SP]

        # get value at top of stack
        value = memory[top_of_stack_addr]

        # increment sp
        registers[SP] += 1

        return value

running = True

# for b in memory:
#     if b == 1:
#         print("Beej!")
    
#     elif b == 2:
#         break

#     else:
#         print(f"Unknown instruction {b}")

while running:
    ir = memory[pc]  # "Instruction Register": holds copy of the currently-executing instruction

    if ir == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    
    elif ir == HALT:
        running = False

    elif ir == SAVE_REG:  # save reg
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        registers[reg_num] = value
        print(registers)
        pc += 3  # must allows increment pc by total operands -- in this case, 3

    elif ir == PRINT_REG:  # print reg
        reg_num = memory[pc + 1]
        print(registers[reg_num])
        pc += 2

    elif ir == PUSH:  # PUSH
        # Decrement SP
        registers[SP] -= 1

        # Get reg num
        reg_num = memory[pc + 1]

        # get value to push
        value = registers[reg_num]

        # copy value to SP
        top_of_stack_addr = registers[SP]
        memory[top_of_stack_addr] = value

        pc += 2

    elif ir == POP:   # POP
        # get reg to pop into
        reg_num = memory[pc + 1]

        # get top of stack addr
        top_of_stack_addr = registers[SP]

        # get value at top of stack
        value = memory[top_of_stack_addr]

        # store value in register
        registers[reg_num] = value

        # increment stack pointer
        registers[SP] += 1
        pc += 2

    elif ir == CALL:
        # compute return addr
        return_addr = pc + 2

        # push return addr on stack
        push_value(return_addr)

        # get value from operand reg
        reg_num = memory[pc + 1]
        value = registers[reg_num
        ]
        # set pc to that value
        pc = value


    else:
        print(f"Unknown instruction {ir}")
        sys.exit(3)
        # pc += 1

    """
    # For the LS-8 to move the PC
    inst_sets_pc = (ir >> 4) & 1 == 1:
    inst_sets_pc = ir & 16 != 0
    inst_sets_pc = ir & 16 # Does this work?


    if not inst_sets_pc:

        number_of_operands = (irt & 0b11000000) >> 6

        how_far_to_move_pc = number_of_operands + 1

        pc += how_far_to_move_pc
    """