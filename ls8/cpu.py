"""CPU functionality."""

import sys
import time

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = False  # Whether our computer is on or off - default state is
        self.ram = [0] * 256  # Attributes space for memory - 256 bits
        self.iv = self.ram[0xF8]  # set up memory for interupt vector
        self.registers = [0] * 8  # Creates list of length 8 to store our registers
        self.registers[7] = 0xF4  # set stack starting point address
        # self.registers[4] = 0b00000000  # set flag register to contain 8 bits
        # self.registers[6] = 0b00000000  # set interupt status register to contain 8 bits
        self.pc = 0  # sets our program counter location- points to the address of currently executing instruction
        self.fl = 0  # Flags - '00000LGE'
        self.ir = None  # Instruction Register: Holds copy of currently running instruction - default is None
       
        self.mar = 2  # Memory Address Register - holds memory address we are reading/writing
        self.mdr = 3  # memory data register - holds value to write or just read
        self.im = 5  # interrupt mask
        self.ie = 6 # interupt status
        self.sp = 7 # stack pointer
        self.code_instruction_pair = {0b10100000 : "ADD",
                                      0b10101000 : "AND",
                                      0b01010000 : "CALL",
                                      0b10100111 : "CMP",
                                      0b01100110 : "DEC",
                                      0b10100011 : "DIV",
                                      0b00000001 : "HLT",
                                      0b01100101 : "INC",
                                      0b01010010 : "INT",
                                      0b00010011 : "IRET",
                                      0b01010101 : "JEQ",
                                      0b01011010 : "JGE",
                                      0b01010111 : "JGT",
                                      0b01011001 : "JLE",
                                      0b01011000 : "JLT",
                                      0b01010100 : "JMP",
                                      0b01010110 : "JNE",
                                      0b10000011 : "LD",
                                      0b10000010 : "LDI",
                                      0b10100100 : "MOD",
                                      0b10100010 : "MUL",
                                      0b00000000 : "NOP",
                                      0b01101001 : "NOT",
                                      0b10101010 : "OR",
                                      0b01000110 : "POP",
                                      0b01001000 : "PRA",
                                      0b01000111 : "PRN",
                                      0b01000101 : "PUSH",
                                      0b00010001 : "RET",
                                      0b10101100 : "SHL",
                                      0b10101101 : "SHR",
                                      0b10000100 : "ST",
                                      0b10100001 : "SUB",
                                      0b10101011 : "XOR",
                                      0b10101111 : "ADDI"
                             }
                        
        self.instruction_branch = {}
        self.instruction_branch["LDI"] = self.handle_ldi
        self.instruction_branch["PRN"] = self.handle_prn
        self.instruction_branch["HLT"] = self.handle_hlt
        self.instruction_branch["POP"] = self.handle_pop
        self.instruction_branch["PUSH"] = self.handle_push
        self.instruction_branch["ST"] = self.handle_store
        self.instruction_branch["RET"] = self.handle_ret
        self.instruction_branch["PRA"] = self.handle_pra
        self.instruction_branch["NOP"] = self.handle_nop
        self.instruction_branch["CALL"] = self.handle_call
        self.instruction_branch["JMP"] = self.handle_jmp
        self.instruction_branch["LD"] = self.handle_ld
        self.instruction_branch["INT"] = self.handle_int
        self.instruction_branch["JEQ"] = self.handle_jeq
        self.instruction_branch["JGE"] = self.handle_jge
        self.instruction_branch["JGT"] = self.handle_jgt
        self.instruction_branch["JLE"] = self.handle_jle
        self.instruction_branch["JLT"] = self.handle_jlt
        self.instruction_branch["JNE"] = self.handle_jne
        self.instruction_branch["IRET"] = self.handle_iret

        self.instruction_branch["MUL"] = self.alu
        self.instruction_branch["ADD"] = self.alu
        self.instruction_branch["DIV"] = self.alu
        self.instruction_branch["SUB"] = self.alu
        self.instruction_branch["AND"] = self.alu
        self.instruction_branch["OR"] = self.alu
        self.instruction_branch["XOR"] = self.alu
        self.instruction_branch["NOT"] = self.alu
        self.instruction_branch["SHL"] = self.alu
        self.instruction_branch["SHR"] = self.alu
        self.instruction_branch["MOD"] = self.alu
        self.instruction_branch["CMP"] = self.alu
        self.instruction_branch["DEC"] = self.alu
        self.instruction_branch["INC"] = self.alu
        self.instruction_branch["ADDI"] = self.alu
        self.instruction = None
        self.operand_a = None
        self.operand_b = None
        self.interrupt_tracker = True

    def ram_read(self, address):
        # `ram_read()` should accept the address to read and return the value stored
        # there.
        return self.ram[address]

    def ram_write(self, value, address):
        # `ram_write()` should accept a value to write, and the address to write it to.
        self.ram[address] = value 
    
    def load(self):
        """Load a program into memory."""

        address = self.pc

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        program = []

        if not sys.argv[1].startswith("examples"):
            print(f"I'm sorry, that is not a valid command line path: {sys.argv[1]}")
            exit()
        with open(sys.argv[1], 'r') as program_path:
            # remove blank lines
            lines = list(line for line in (l.strip() for l in program_path) if line and not line.startswith("#"))

            for line in lines:
                for i in range(len(line)):
                    if line[i] == "#":
                        line = line[:i-1]
                        break
                program.append(int(line, 2))

        
        for instruction in program:
            # print(instruction)
            self.ram[address] = instruction
            address += 1


    def alu(self):
        """ALU operations."""

        alu_instruction_branch = {}
        alu_instruction_branch["MUL"] = self.handle_mul
        alu_instruction_branch["ADD"] = self.handle_add
        alu_instruction_branch["DIV"] = self.handle_div
        alu_instruction_branch["SUB"] = self.handle_sub
        alu_instruction_branch["AND"] = self.handle_and
        alu_instruction_branch["OR"] = self.handle_or
        alu_instruction_branch["XOR"] = self.handle_xor
        alu_instruction_branch["NOT"] = self.handle_not
        alu_instruction_branch["SHL"] = self.handle_shl
        alu_instruction_branch["SHR"] = self.handle_shr
        alu_instruction_branch["MOD"] = self.handle_mod
        alu_instruction_branch["CMP"] = self.handle_cmp
        alu_instruction_branch["DEC"] = self.handle_dec
        alu_instruction_branch["INC"] = self.handle_inc
        alu_instruction_branch["ADDI"] = self.handle_addi

        alu_instruction_branch[self.ir]()

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X %02s| " % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2),
            self.code_instruction_pair[self.ram[self.pc]],
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def handle_ldi(self):
        self.registers[self.operand_a] = self.operand_b

    def handle_prn(self):
        print(self.registers[self.operand_a])
    
    def handle_mul(self):
        val = self.registers[self.operand_a] * self.registers[self.operand_b]
        self.registers[self.operand_a] = val & 0xFF

    def handle_hlt(self):
        self.running = False

    def push_value(self, val):
        # decrement sp
        self.registers[self.sp] -= 1

        # get top of stack
        top_stack = self.registers[self.sp]

        # copy value to sp
        self.ram[top_stack] = val

    def pop_value(self):
        # get top of stack
        top_stack = self.registers[self.sp]

        # get value at top of stack
        value = self.ram[top_stack]

        # increment sp
        self.registers[self.sp] += 1

        return value

    def handle_pop(self):
        # get address for top of stack
        top_stack = self.registers[self.sp]
        # get value at top of stack
        value = self.ram[top_stack]
        # store value in register
        self.registers[self.operand_a] = value
        # increment stack pointer
        self.registers[self.sp] += 1

    def handle_push(self):
        # decrement sp
        self.registers[self.sp] -= 1
        # get value to add to register
        value = self.registers[self.operand_a]
        # get address for top of stack
        top_stack = self.registers[self.sp]
        # copy value to sp
        self.ram[top_stack] = value

    def handle_store(self):
        self.ram[self.operand_a] = self.registers[self.operand_b]

    def handle_add(self):
        val = self.registers[self.operand_a] + self.registers[self.operand_b]
        self.registers[self.operand_a] = val & 0xFF

    def handle_div(self):
        try:
            val = self.registers[self.operand_a] // self.registers[self.operand_b]
            self.registers[self.operand_a] = val & 0xFF
        except ZeroDivisionError:
            print("Unable to divide by zero.")
            exit()

    def handle_sub(self):
        val = self.registers[self.operand_a] - self.registers[self.operand_b]
        self.registers[self.operand_a] = val & 0xFF

    def handle_and(self):
        self.registers[self.operand_a] &= self.registers[self.operand_b]

    def handle_or(self):
        self.registers[self.operand_a] |= self.registers[self.operand_b]

    def handle_xor(self):
        self.registers[self.operand_a] ^= self.registers[self.operand_b]

    def handle_not(self):
        self.registers[self.operand_a] = ~self.registers[self.operand_a]

    def handle_shl(self):
        self.registers[self.operand_a] <<= self.registers[self.operand_b]

    def handle_shr(self):
        self.registers[self.operand_a] >>= self.registers[self.operand_b]

    def handle_ret(self):
        # get value at top of stack
        self.pc = self.pop_value()

    def handle_pra(self):
        character = chr(self.registers[self.operand_a])
        print(ord(character))

    def handle_nop(self):
        return

    def handle_call(self):
        # computer return addr
        return_addr = self.pc + 2

        # push return addr on stack
        self.push_value(return_addr)

        # get value from operand reg
        reg_num = self.ram[self.pc + 1]
        value = self.registers[reg_num]

        # set pc to that value
        self.pc = value

    def handle_jmp(self):
        self.pc = self.registers[self.operand_a]

    def handle_ld(self):
        memory_address = self.registers[self.operand_b]
        self.registers[self.operand_a] = self.ram[memory_address]

    def handle_mod(self):
        try:
            self.registers[self.operand_a] %= self.registers[self.operand_b]
        except ZeroDivisionError:
            print("Unable to divide by zero.")
            exit()

    def handle_cmp(self):
        if self.registers[self.operand_a] == self.registers[self.operand_b]:
            self.fl = 0b00000001

        elif self.registers[self.operand_a] > self.registers[self.operand_b]:
            self.fl = 0b00000010

        elif self.registers[self.operand_a] < self.registers[self.operand_b]:
            self.fl = 0b00000100

        else:
            self.fl = 0b00000000

    def handle_dec(self):
        val = self.registers[operand_a] - 1
        self.registers[operand_a] = val & 0xFF

    def handle_inc(self):
        val = self.registers[operand_a] + 1
        self.registers[operand_a] = val & 0xFF

    def handle_jeq(self):
        if self.fl & 1 == 1:
            self.pc = self.registers[self.operand_a]
        else:
            self.pc += 2

    def handle_jge(self):
        if self.fl & 2 == 2 | self.fl & 1 == 1: 
            self.pc = self.registers[self.operand_a]
        else:
            self.pc += 2

    def handle_jgt(self):
        if self.fl & 2 == 2: 
            self.pc = self.registers[self.operand_a]
        else:
            self.pc += 2

    def handle_jle(self):
        if self.fl & 4 == 4 | self.fl & 1 == 1: 
            self.pc = self.registers[self.operand_a]
        else:
            self.pc += 2

    def handle_jlt(self):
        if self.fl & 4 == 4: 
            self.pc = self.registers[self.operand_a]
        else:
            self.pc += 2

    def handle_jne(self):
        if self.fl & 1 == 0: 
            self.pc = self.registers[self.operand_a]
        else:
            self.pc += 2

    def handle_int(self):
        masked_int = self.registers[self.im] & self.registers[self.ie]
        for i in range(8):
            interrupt_happened = ((masked_int >> i) & 1) == 1
            if masked_int & interrupt_happened:
                self.interrupt_tracker = False
                self.registers[self.ie] = self.registers[self.ie] & ~interrupt_happened
                self.push_value(self.pc)
                self.push_value(self.fl)
                for reg in range(7):
                    self.push_value(self.registers[reg])
                self.pc = self.ram[self.iv + i]

    def handle_iret(self):
        for reg in range(6, -1, -1):
            self.registers[reg] = self.pop_value()
        self.fl = self.pop_value()
        self.pc = self.pop_value()
        self.interrupt_tracker = True

    def handle_addi(self):
        self.registers[self.operand_a] += self.operand_b
  
    def set_pc(self):

        if (self.instruction >> 4) & 1 == 1:
            return

        else:
            if (self.instruction >> 6) & 1 == 1:
                self.pc += 2

            elif (self.instruction >> 6) & 2 == 2:
                self.pc += 3

            else:
                self.pc += 1

    def run(self):
        """Run the CPU."""
        self.running = True
        start_time = time.time()
        time_interval = 0

        while self.running:
            loop_time = time.time()
            time_interval += (loop_time - start_time)
            start_time = loop_time
            if time_interval >= 1:
                self.registers[self.ie] = 1
                time_interval = 0
            self.instruction = self.ram[self.pc]
            self.operand_a = self.ram_read(self.pc+1)
            self.operand_b = self.ram_read(self.pc+2) 
            self.ir = self.code_instruction_pair[self.instruction]
            self.instruction_branch[self.ir]()
            self.set_pc()

            if self.interrupt_tracker:
                self.handle_int()

        exit()
