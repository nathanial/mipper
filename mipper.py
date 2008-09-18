import logging
import parser

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(message)s',
                    filename='mipper.log',
                    filemode='w')

class Register:
    def __init__(self): self.value = 0
    def __cmp__(self, that): return self.value.__cmp__(that)
    def setValue(self, value): self.value = value
    def getValue(self): return self.value

class Program:
    def __init__(self, text):
        allocations, instructions = parser.parse("program", text)
        self.state = State(instructions, allocations)

    def execute(self):
        self.state.allocateMemory()
        while self.state.hasNextInstruction():
            self.state.executeNextInstruction()


class State:

    def __init__(self, instructions, allocations):
        regs = ["$at", "$gp", "$sp" "$fp", "$ra", "$zero", "$hi", "$lo", "$pc"]
        regs.extend(self.create_registers("$v", 1))
        regs.extend(self.create_registers("$a", 3))
        regs.extend(self.create_registers("$t", 9))
        regs.extend(self.create_registers("$s", 7))
        regs.extend(self.create_registers("$k", 1))
        self.registers = dict(map(lambda reg: [reg, Register()], regs))
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
        else:
            instruction.execute(self)
            self.incrementProgramCounter()

    def isLabel(self, instruction): return type(instruction) is str

    def hasNextInstruction(self):
        return self.programCounter() < len(self.instructions)

    def currentInstruction(self):
        return self.instructions[self.programCounter().getValue()]

    def programCounter(self):
        return self.registers["$pc"]

    def incrementProgramCounter(self):
        current_val = self.programCounter().getValue()
        self.programCounter().setValue(current_val + 1)

def AssignmentOp(dst, reg1, reg2):
    def f(meth):
        def g(obj, state):
            val1 = state.registers[obj.__getattribute__(reg1)].getValue()
            val2 = state.registers[obj.__getattribute__(reg2)].getValue()
            result = meth(val1, val2)
            state.registers[obj.__getattribute__(dst)].setValue(result)
        return g
    return f

def AssignmentImmediate(dst, reg1, im):
    def f(meth):
        def g(obj, state):
            val1 = state.registers[obj.__getattribute__(reg1)].getValue()
            val2 = obj.__getattribute__(im)
            result = meth(val1, val2)
            state.registers[obj.__getattribute__(dst)].setValue(result)
        return g
    return f

def AssignHiLo(reg1, reg2):
    def f(meth):
        def g(obj, state):
            val1 = state.registers[obj.__getattribute__(reg1)].getValue()
            val2 = state.registers[obj.__getattribute__(reg2)].getValue()
            hi, lo = meth(val1, val2)
            state.registers["$hi"].setValue(hi)
            state.registers["$lo"].setValue(lo)
        return g
    return f
