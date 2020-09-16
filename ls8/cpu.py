"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = False  # Whether our computer is on or off - default state is
        self.ram = [0] * 256  # Attributes space for memory - 256 bits
        self.registers = [0] * 8  # Creates list of length 8 to store our registers
        self.pc = self.registers[0]  # sets our program counter - points to the address of currently executing instruction
        self.ir = self.registers[1]  # Instruction Register: Holds copy of currently running instruction - default is None
        self.mar = self.registers[2]  # Memory Address Register - holds memory address we are reading/writing
        self.mdr = self.registers[3]  # memory data register - holds value to write or just read
        self.fl = self.registers[4]  # Flags
        self.im = self.registers[5]  # interrupt mask
        self.ie = self.registers[6]  # interupt status
        self.sp = self.registers[7]  # stack pointer
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
                                      0b10101011 : "XOR"
                             }


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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            #     It needs to read the memory address that's stored in register `PC`, and store
            # that result in `IR`, the _Instruction Register_. This can just be a local
            # variable in `run()`.
            instruction = self.ram[self.pc]
            self.ir = self.code_instruction_pair[instruction]
            # Some instructions requires up to the next two bytes of data _after_ the `PC` in
            # memory to perform operations on. Sometimes the byte value is a register number,
            # other times it's a constant value (in the case of `LDI`). Using `ram_read()`,
            # read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and
            # `operand_b` in case the instruction needs them.
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            # Then, depending on the value of the opcode, perform the actions needed for the
            # instruction per the LS-8 spec. Maybe an `if-elif` cascade...? There are other
            # options, too.
            if self.ir == "LDI":
                self.registers[operand_a] = operand_b
                self.pc += 3
            elif self.ir == "PRN":
                print(self.registers[operand_a])
                self.pc += 2
            elif self.ir == "MUL":
                self.registers[operand_a] *= self.registers[operand_b]
                self.pc += 3
            elif self.ir == "HLT":
                self.running = False
            
        exit()

            # After running code for any particular instruction, the `PC` needs to be updated
            # to point to the next instruction for the next iteration of the loop in `run()`.
            # The number of bytes an instruction uses can be determined from the two high bits
            # (bits 6-7) of the instruction opcode. See the LS-8 spec for details.
            #         pass

if __name__ == "__main__":
    cpu = CPU()
    cpu