import logging
from Mipper import parser

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(message)s',
                    filename='mipper.log',
                    filemode='w')

class ProgramSuspension: pass

class Register:
    def __init__(self): self.value = 0
    def __cmp__(self, that): return self.value.__cmp__(that)
    def setValue(self, value): self.value = value
    def getValue(self): return self.value

class Program:
    def __init__(self, text):
        allocations, instructions = parser.parse("program", text)
        self.state = State(instructions, allocations)
        self.on_suspension = lambda state : None

    def execute(self):
        self.state.allocateMemory()
        while self.state.hasNextInstruction():
            try:
                self.state.executeNextInstruction()
            except ProgramSuspension:
                self.on_suspension(self.state)
                break

class State:

    def __init__(self, instructions, allocations):
        regs = ["$at", "$gp", "$sp" "$fp", "$ra",
                "$zero", "$hi", "$lo", "$pc"]
        regs.extend(self.create_registers("$v", 1))
        regs.extend(self.create_registers("$a", 3))
        regs.extend(self.create_registers("$t", 9))
        regs.extend(self.create_registers("$s", 7))
        regs.extend(self.create_registers("$k", 1))
        regs.extend(self.create_registers("$f", 12))
        self.registers = dict(map(lambda reg: [reg, Register()], regs))
        self.registers["$ra"].setValue(-1)
        self.instructions = instructions
        self.allocations = allocations
        self.memory = []
        self.labels = {}

    def allocateMemory(self):
        for a in self.allocations:
            a.allocate(self)

    def create_registers(self, prefix, n):
        regs = []
        for i in range(0, n + 1):
            regs.append(prefix + str(i))
        return regs

    def executeNextInstruction(self):
        instruction = self.currentInstruction()
        if self.isLabel(instruction):
            self.incrementProgramCounter()
            self.executeNextInstruction()
        elif self.isBreak(instruction):
            self.incrementProgramCounter()
            self.suspendExecution()
        else:
            logging.debug("executing " + str(instruction))
            instruction.execute(self)
            self.incrementProgramCounter()

    def isLabel(self, instruction):
        return (type(instruction) is str) and (instruction != "BREAK")

    def isBreak(self, instruction):
        return instruction == "BREAK"

    def suspendExecution(self):
        response = raw_input("Continue?")
        if response == "y":
            self.executeNextInstruction()
        else:
            raise ProgramSuspension()

    def hasNextInstruction(self):
        return self.programCounter() < len(self.instructions)

    def currentInstruction(self):
        return self.instructions[self.programCounter()]

    def programCounter(self):
        return self.registers["$pc"].getValue()

    def incrementProgramCounter(self):
        current_val = self.programCounter()
        self.setRegister("$pc", current_val + 1)

    def setRegister(self, reg, val):
        self.registers[reg].setValue(val)

    def getRegister(self, reg):
        return self.registers[reg].getValue()
