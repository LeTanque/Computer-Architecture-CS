"""CPU functionality."""
import sys

class CPU:
    def __init__(self):     # Construct a new CPU
        self.pc = 0                         #: Program Counter
        self.ir = None                      #: Instruction Register

        self.ram = [0] * 256                #: Init as array of zeros
        self.reg = [0] * 8                  #: Register fixed number
        
        self.fl = { "RUNNING": False }      #: Flags

    def load(self):
        # Load a program into memory. First method called from ls8
        address = 0                     

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

    # Arithmatic and logic unit
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            pass
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, counter):        #: Read the ram
        return self.ram[counter]
    
    def ram_write(self, payload):       #: Write the ram
        pass

    def trace(self):
        print(f"\nTRACE: %02X | %02X %02X %02X %02X \n" % (
            self.pc,        #: 0
            #self.fl,       #: Flags
            #self.ie,       #: Might have something to do with interrupts
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2),
            self.ram_read(self.pc + 3)
        ), end='')

        for i in range(8):
            print(": %02X" % self.reg[i], end='\n')

        print()

    def run(self):
        self.fl["RUNNING"] = True
        self.trace()
        self.fl["RUNNING"] = False
