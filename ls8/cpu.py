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
        self.french = 0         #: French Finish Mode?

        self.opcodes = {
            NOP: self.NOP,
            # HLT: self.HLT,
            LDI: self.LDI,
            PRN: self.PRN,
            POP: self.POP,
            PUSH: self.PUSH,
            END: self.END,
            JMP: self.JMP,
            JEQ: self.JEQ,
            JNE: self.JNE
        }

        self.alucodes = { MUL }
        
        self.load(program)
    
    def END(self):
        if self.french == 1:
            print("\n\n\n   FIN\n\n\n")
        else:
            print("\n    END OF PROGRAM\n")
        exit(1)
    
    def HLT(self):
        if self.french == 1:
            print("\nL' HALTE")
        else:
            print("HALT")
        self.END()
    
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

    def JMP(self, reg_a, reg_b):
        pass

    def JEQ(self, register, reg_b):
        pass
    
    def JNE(self, register, reg_b):
        pass


    def load(self, proggy):
        # Load a program into memory. First method called from ls8
        address = 0                     

        with open(proggy, 'r') as program:
            for line in program:
                short_line = line[:8]
                strip = re.sub(r'(?m)^ *#.*\n?', '', str(short_line))
                if len(strip) > 0 and strip is not "\n":
                    command = int(strip, 2)
                    print('CMD:', bin(command))
                    self.ram_write(address, command)
                    address += 1
        
        self.run()
            

    # Arithmatic and logic unit ALU
    def alu(self, operation, reg_a, reg_b):
        if operation == ADD:     #: Add
            if self.verbose == 1:
                print(f"Adding reg {reg_a} and reg {reg_b}")
            self.reg[reg_a] += self.reg[reg_b]

        elif operation == SUB:   #: Sub
            if self.verbose == 1:
                print(f"Subtracting reg {reg_b} from reg {reg_a}")
            self.reg[reg_a] -= self.reg[reg_b]
        
        elif operation == CMP:   #: Compare, if equal, set E to 1
            print("CMP triggers")
            if self.verbose == 1:
                print(f"Comparing reg {reg_b} and reg {reg_a}")
            if self.reg[reg_a] < self.reg[reg_b]:
                if self.verbose == 1:
                    print("Less than")
            elif self.reg[reg_a] > self.reg[reg_b]:
                if self.verbose == 1:
                    print("Greater than")
            elif self.reg[reg_a] == self.reg[reg_b]:
                if self.verbose == 1:
                    print("Equal")

        elif operation == MUL:     #: Mult
            print("Multi triggers")
            if self.verbose >= 1:
                print(f"Multiplying reg {reg_a} and reg {reg_b}")
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, counter):        #: Read the ram
        return self.ram[counter]
    
    def ram_write(self, address, payload):       #: Write the ram
        if self.verbose == 1:
            print(f"RAM_WRITE: {self.ram[address]}: {payload}")
        self.ram[address] = payload

    def trace(self):
        print("\n\n > BEGIN TRACE ======================")
        print(f"TRACE: %02X | %02X %02X %02X %02X | Flags: %02X" % (
            self.pc,                    #: 0
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2),
            self.ram_read(self.pc + 3),
            self.fl[0],                 #: Flags, might be doing this wrong
            #self.ie,           #: Might have something to do with interrupts
        ), end=' \n')

        print("\nREGISTERS:")
        for i in range(8):
            if self.reg[i] > 0:
                print(f"R{i}: %s" % self.reg[i], end="\n")
        print(" >>> END TRACE <<< =======================\n")

    def run(self):
        self.running = 1
        self.verbose = 2
        self.french = 1

        # If verbosity 1+, trace the first op
        if self.verbose >= 1:
            self.trace()

        while self.running == 1:
            self.ir = self.ram_read(self.pc)
            
            if self.ir in self.opcodes.keys() or self.ir in self.alucodes:
                op_a = self.ram_read(self.pc + 1)
                op_b = self.ram_read(self.pc + 2)
                check_end = self.ram_read(self.pc + 3)

                if self.verbose >= 1:
                    print('op_a: ', bin(op_a))
                    print('op_b: ', bin(op_b))
                    print('check_end: ', bin(check_end))

                if self.pc >= (len(self.ram) - 1):
                    self.running = 0
                    self.END()

                if self.ir in self.opcodes.keys():
                    self.opcodes[self.ir](op_a, op_b)
                
                if self.ir in self.alucodes:
                    print(bin(self.ir))
                    self.alu(self.ir, op_a, op_b)

                if op_b == HLT and check_end == 0:
                    self.HLT()

                # If verbosity 2+, trace every operation
                if self.verbose == 2 and self.ir in self.opcodes.keys():
                    print(f"{self.opcodes[self.ir].__name__}  op_a: {bin(op_a)}  op_b: {bin(op_b)}")
                    self.trace()

            self.pc += 1
        self.running = 0


# * **immediate**: takes a constant integer value as an argument
# * **register**: takes a register number as an argument
HLT = 0b1           #: HALT
END = 0b11111111    #: END
LDI = 0b10000010    #: LDI register immediate set value of reg to an int
PRN = 0b01000111    #: Print decimal
PRA = 0b01001000    #: Pseudo-instruction, Print alpha character value stored in the given register.
NOP = 0b0           #: No Operation, do nothing with this instruction

# Flag bits 
FLL = 0b00000100     #: Less than
FLG = 0b00000010     #: Greater than
FLE = 0b00000001     #: Equal to

# Writes or reads from memory
LD = 0b10000011     #: Loads RegA with val at RegB
ST = 0b10000100     #: Store value in registerB in the address stored in registerA. 

# stack
POP = 0b01000110    #: Pop off register
PUSH = 0b01000101   #: Push on register

CALL = 0b01010000   #: Call register, Calls a subroutine (function) at the address stored in the register.
RET = 0b00010001    #: RETURn, return from subroutine.

# Cool new commands
JMP = 0b01010100    #: Jump jump, kriss kross will make ya
JEQ = 0b01010101    #: Jump, if equal, to address
JNE = 0b01010110    #: Jump, if not equal, to address

# ALU Ops
MUL = 0b10100010    #: Multiply
OR = 0b10101010     #: OR
NOT = 0b01101001    #: NOT
CMP = 0b10100111    #: Compare the values of two registers
ADD = 0b10100000    #: Add
SUB = 0b10100001    #: Subtract

