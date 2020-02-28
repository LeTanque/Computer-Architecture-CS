"""CPU functionality."""
import sys
import re


class CPU:
    def __init__(self, program):         # Construct a new CPU
        self.pc = 0             #: Program Counter
        self.ir = None          #: Instruction Register - currently running instruction

        self.ram = [0] * 256    #: Init as array of zeros
        self.reg = [0] * 8      #: Register fixed number
        
        self.fl = [0] * 8       #: Flags

        self.mar = [0] * 8      #: Memory Address Reader

        self.running = 0        #: Running?
        self.verbose = 0        #: Verbosity?

        self.opcodes = {
            NOP: self.NOP,
            HLT: self.HLT,
            LDI: self.LDI,
            PRN: self.PRN,
            POP: self.POP,
            PUSH: self.PUSH,
            END: self.END
        }
        self.load(program)
    
    def HLT(self):
        print("HALT")
        exit(1)
    
    def END(self):
        print("END")
        exit(1)
    
    def NOP(self, op_a, op_b):
        pass

    def LDI(self, op_a, op_b):
        print(f"LDI register set: {op_a}:{op_b}")
        self.reg[op_a] = op_b

    def PRN(self, register, op_b):
        print(f'Printing decimal at register {register}:', self.reg[register])

    def POP(self, op_a, op_b):
        pass

    def PUSH(self, op_a, op_b):
        pass

    def load(self, proggy):
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

        with open(proggy, 'r') as program:
            for line in program:
                short_line = line[:8]
                strip = re.sub(r'(?m)^ *#.*\n?', '', str(short_line))
                if len(strip) > 0 and strip is not "\n":
                    command = int(strip, 2)
                    print('command: ', bin(command))
                    self.ram_write(address, command)
                    address += 1
        
        self.run()
            

    # Arithmatic and logic unit
    def alu(self, operation, reg_a, reg_b):
        """ALU operations."""
        if operation == 0b10100000:     #: Add
            if self.verbose == 1:
                print(f"Adding reg {reg_a} and reg {reg_b}")
            self.reg[reg_a] += self.reg[reg_b]

        elif operation == 0b10100001:   #: Sub
            if self.verbose == 1:
                print(f"Subtracting reg {reg_b} from reg {reg_a}")
            self.reg[reg_a] -= self.reg[reg_b]

        elif operation == MUL:     #; Mult
            if self.verbose == 1:
                print(f"Multiplying reg {reg_a} and reg {reg_b}")
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, counter):        #: Read the ram
        return self.ram[counter]
    
    def ram_write(self, address, payload):       #: Write the ram
        if self.verbose == 1:
            print(f"RAM_WRITE: {self.ram[address]}: {payload}")
        self.ram[address] = payload

    def trace(self):
        print("\n=== > BEGIN TRACE < ======================")
        print(f"\nTRACE: %02X | %02X %02X %02X %02X | Flags: %02X" % (
            self.pc,                    #: 0
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2),
            self.ram_read(self.pc + 3),
            self.fl[0],                 #: Flags, might be doing this wrong
            #self.ie,           #: Might have something to do with interrupts
        ), end=' \n')

        print("\n\nREGISTERS:")
        for i in range(8):
            print(f"{i}: %02X" % self.reg[i], end="\n")
        print("\n=== > END TRACE < =========================\n\n")

    def run(self):
        self.running = 1
        self.verbose = 1

        if self.verbose == 1:
            self.trace()

        while self.running == 1:
            self.ir = self.ram_read(self.pc)

            if self.pc >= (len(self.ram) - 1):
                self.running = 0
                self.END()
            if self.opcodes[self.ir].__name__ is "HLT":
                print("Halty")
                self.HLT()
                break

            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            if self.ir in self.opcodes.keys():
                self.opcodes[self.ir](op_a, op_b)

            if self.verbose == 2:
                print(f"{self.opcodes[self.ir].__name__}: op_a:{bin(op_a)} op_b:{bin(op_b)}")
                self.trace()
            self.pc += 3
        self.running = 0


# * **immediate**: takes a constant integer value as an argument
# * **register**: takes a register number as an argument
HLT = 0b1           #: HALT
END = 0b11111111    #: END
LDI = 0b10000010    #: LDI register immediate set value of reg to an int
PRN = 0b01000111    #: Print decimal
PRA = 0b01001000    #: Pseudo-instruction, Print alpha character value stored in the given register.
NOP = 0b0           #: No Operation, do nothing with this instruction

# Writes or reads from memory
LD = 0b10000011     #: Loads RegA with val at RegB
ST = 0b10000100     #: Store value in registerB in the address stored in registerA. 

# stack
POP = 0b01000110    #: Pop off register
PUSH = 0b01000101   #: Push on register

CALL = 0b01010000   #: Call register, Calls a subroutine (function) at the address stored in the register.
RET = 0b00010001    #: RETURn, return from subroutine.

# ALU Ops
MUL = 0b10100010    #: Multiply
OR = 0b10101010     #: OR
NOT = 0b01101001    #: NOT

