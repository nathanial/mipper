import logging
import parser

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
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)

class ProgramFactory:
    def __init__(self, input, output, on_suspension):
        self.input = input
        self.output = output
        self.on_suspension = on_suspension

    def create_program(self, text, **kwargs):
        program = Program(text)
        program.state._in = kwargs.get('input') or self.input
        program.state._out = kwargs.get('output') or self.output
        program.on_suspension = kwargs.get('on_suspension') or self.on_suspension
        return program

class Program:
    def __init__(self, text):
        allocations, instructions = parser.parse("program", text)
        self.state = State(instructions, allocations)
        self.on_suspension = lambda state : None

    def execute(self):
        self.allocateMemory()
        self.executeInstructions()

    def allocateMemory(self):
        for a in self.state.allocations:
            a.allocate(self.state)

    def executeInstructions(self):
        while self.state.hasNextInstruction():
            try:
                self.executeNextInstruction()
            except ProgramSuspension:
                self.on_suspension(self.state)
                break

    def executeNextInstruction(self):
        instruction = self.state.currentInstruction()
        if self.isLabel(instruction):
            self.state.incrementProgramCounter()
            self.executeNextInstruction()
        elif self.isBreak(instruction):
            self.state.incrementProgramCounter()
            self.suspendExecution()
        else:
            logging.debug("executing " + str(instruction))
            instruction.execute(self.state)
            self.state.incrementProgramCounter()
            # instructions rely on value of programCounter()
            # increment only after instruction.execute

    def suspendExecution(self):
        raise ProgramSuspension()

    def isLabel(self, instruction):
        return (type(instruction) is str) and (instruction != "BREAK")

    def isBreak(self, instruction):
        return instruction == "BREAK"

class State:
    def __init__(self, instructions, allocations):
        self.registers = {}
        self.create_register("$zero", at = 0)
        self.create_register("$at", at = 1)
        self.create_registers("$v", _from = 2, _to = 3)
        self.create_registers("$a", _from = 4, _to = 7)
        self.create_registers("$t", _from = 8, _to = 15)
        self.create_registers("$s", _from = 16, _to = 23)
        self.create_registers("$t", numeral = 8, _from = 24, _to = 25)
        self.create_registers("$k", _from = 26, _to = 27)
        self.create_register("$gp", at = 28)
        self.create_register("$sp", at = 29)
        self.create_register("$fp", at = 30)
        self.create_register("$ra", at = 31)
        self.create_register("$pc")
        self.create_register("$hi")
        self.create_register("$lo")

        self.setRegister("$ra", -1)
        self.instructions = instructions
        self.allocations = allocations
        self.memory = []
        self.labels = {}


    def create_register(self, name, at = -1):
        reg = Register()
        self.registers.update([[name, reg], ["$" + str(at), reg]])

    def create_registers(self, prefix, _from, _to, numeral = 0):
        for i in range(_from, _to + 1):
            offset = i - _from
            name = prefix + str(numeral + offset)
            reg = Register()
            self.registers.update([[name, reg], ["$" + str(i), reg]])

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
