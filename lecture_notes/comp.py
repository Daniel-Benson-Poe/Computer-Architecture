# These all mean the same thing:
#### Index into the memory array
#### Address
#### Location
#### Pointer

## operands == arguments to the instruction

memory = [
    1,  # print Beej  address 0
    3,  # save_reg R1, 37
    1,
    37,
    4,  # print reg
    1,  # R1
    2,  # halt
]

registers = [0] * 8  # R0-R7

# Variables in hardware.. Known as "registers".
# There are a fixed number of registers - we can't make more beyond manufacturing a new chip that has more
# They have fixed names
# R0, R1, R2, ..., R6, R7

pc = 0  # "Program Counter": address of the currently-executing instruction

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

    if ir == 1:
        print("Beej!")
        pc += 1
    
    elif ir == 2:
        running = False

    elif ir == 3:  # save reg
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        registers[reg_num] = value
        print(registers)
        pc += 3  # must allows increment pc by total operands -- in this case, 3

    elif ir == 4:  # print reg
        reg_num = memory[pc + 1]
        print(registers[reg_num])
        pc += 2

    else:
        print(f"Unknown instruction {ir}")
        pc += 1