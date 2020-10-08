"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False

        # initialize stack pointer(SP) -> F4
        self.reg[7] = 0xF4

        # create branch table
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[POP] = self.handle_POP
        self.branchtable[PUSH] = self.handle_PUSH

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def handle_HLT(self):
        self.running = False
        self.pc = 0

    def handle_LDI(self):
        reg_idx = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)

        self.reg[reg_idx] = value

        self.pc += 3

    def handle_PRN(self):
        reg_idx = self.ram_read(self.pc + 1)
        value = self.reg[reg_idx]

        print(value)

        self.pc += 2

    def handle_MUL(self):
        reg_idx_a = self.ram_read(self.pc + 1)
        reg_idx_b = self.ram_read(self.pc + 2)

        self.alu("MUL", reg_idx_a, reg_idx_b)
        self.pc += 3

    def handle_PUSH(self):
        # 1. Decrement the `SP`.
        self.reg[7] -= 1

        SP = self.reg[7]

        # 2. Copy the value in the given register to the address pointed to by `SP`.

        # Get value from register
        reg_idx = self.ram_read(self.pc + 1)
        value = self.reg[reg_idx]

        # Save to RAM
        self.ram[SP] = value

        # 3. Increment PC
        self.pc += 2

    def handle_POP(self):
        # 1. Copy the value from the address pointed to by `SP` to the given register.
        # Get position of SP
        SP = self.reg[7]

        # Get value from RAM
        reg_idx = self.ram_read(self.pc + 1)
        value = self.ram[SP]

        # Save to register
        self.reg[reg_idx] = value

        # 2. Increment `SP`.
        self.reg[7] += 1

        # 3. Increment PC
        self.pc += 2

    def load(self, input):
        """Load a program into memory."""
        if len(input) != 2:
            print("remember to pass the second file name")
            print("usage: python3 ls8.py <second_file_name.py>")
            sys.exit()

        address = 0

        try:
            with open(input[1]) as file:
                for line in file:
                    if line == '\n' or line[0] == '#':
                        continue

                    integer = int(line[0:8], 2)
                    self.ram[address] = integer

                    address += 1

        except FileNotFoundError:
            print(f'Error from {input[0]}: {input[1]} not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            ir = self.ram_read(self.pc)
            self.branchtable[ir]()

            # OLD CODE 0(N)
            # if ir == LDI:
            #     reg_idx = self.ram_read(self.pc + 1)
            #     value = self.ram_read(self.pc + 2)

            #     self.reg[reg_idx] = value

            #     self.pc += 3

            # elif ir == PRN:
            #     reg_idx = self.ram_read(self.pc + 1)
            #     value = self.reg[reg_idx]

            #     print(value)

            #     self.pc += 2

            # elif ir == MUL:
            #     reg_idx_a = self.ram_read(self.pc + 1)
            #     reg_idx_b = self.ram_read(self.pc + 2)

            #     self.alu("MUL", reg_idx_a, reg_idx_b)
            #     self.pc += 3

            # elif ir == HLT:
            #     self.pc = 0
            #     running = False
