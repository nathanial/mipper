import logging
from Mipper import parser
import copy

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

class ProgramFactory(object):
    def __init__(self, **kwargs):
        for key in kwargs:
            if key == "input_function":
                self.input_function = kwargs[key]
            elif key == "output_function":
                self.output_function = kwargs[key]
            elif key == "on_suspension":
                self.on_suspension = kwargs[key]
            else:
                raise "KWARG not recognized"

    def create_program(self, text):
        program = Program(text)
        program.state._in = self.input_function
        program.state._out = self.output_function
        program.on_suspension = self.on_suspension
        return program


class Program(object):
    def __init__(self, text):
        allocations, instructions = parser.parse("program", text)
        self.state = State(instructions, allocations)

    def execute(self):
        self.allocateMemory()
        self.executeInstructions()

    def allocateMemory(self):
        self.state = reduce(lambda ps, a: a.allocate(ps), self.state.allocations, self.state)

    def executeInstructions(self):
        def execute(state, instruction):
            if state.is_suspended:
                return state
            if self.isLabel(instruction):
                return state.incrementProgramCounter()
            elif self.isBreak(instruction):
                return state.incrementAndSuspend()
            else:
                logging.debug("executing " + str(instruction))
                print instruction
                return instruction.execute(state).incrementProgramCounter()

        self.state = reduce(execute, self.state.instructions, self.state)

    def suspendExecution(self): pass

    def isLabel(self, txt):
        return type(txt) is str and txt != "BREAK"

    def isBreak(self, txt):
        return txt == "BREAK"

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
        self._out = lambda str : None
        self._in = lambda : None
        self.is_suspended = False

    def create_registers(self, prefix, n):
        regs = []
        for i in range(0, n + 1):
            regs.append(prefix + str(i))
        return regs

    def programCounter(self):
        return self.getRegister("$pc")

    def suspend(self):
        state = copy.deepcopy(self)
        state.is_suspended = True
        return state

    def incrementAndSuspend(self):
        return self.incrementProgramCounter().suspend()

    def incrementProgramCounter(self):
        current_val = self.getRegister("$pc")
        return self.setRegister("$pc", current_val + 1)

    def setRegister(self, reg, val):
        state = copy.deepcopy(self)
        state.registers[reg].setValue(val)
        return state

    def getRegister(self, reg):
        return self.registers[reg].getValue()
