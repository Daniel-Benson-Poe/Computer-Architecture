"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # Attributes space for memory - 256 bits
        self.registers = [0] * 8  # Creates list of length 8 to store our registers
        self.pc = 0  # sets our program counter - points to the address of currently executing instruction
        self.running = False  # Whether our computer is on or off - default state is
        self.ir = None  # Instruction Register: Holds copy of currently running instruction - default is None

    def ram_read(self, address):
        # `ram_read()` should accept the address to read and return the value stored
        # there.
        self.pc = address
        return self.ram[self.pc]

    def ram_write(self, value, address):
        # `ram_write()` should accept a value to write, and the address to write it to.
        self.pc = address
        self.ram[self.pc] = value 
    
    def load(self):
        """Load a program into memory."""

        address = self.pc

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
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

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        pass

if __name__ == "__main__":
    cpu = CPU()
    cpu