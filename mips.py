import logging
import parser
import new
from types import MethodType

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(message)s',
                    filename='mipper.log',
                    filemode='w')

class ProgramSuspension: pass

class Register:
    def __init__(self): self.val = 0
    def __cmp__(self, that): return self.val.__cmp__(that.value())
    def set_value(self, val): self.val = val
    def value(self): return self.val
    def __str__(self):
        return str(self.val)
    def __repr__(self):
        return str(self.val)

class ProgramFactory:
    def __init__(self, input, output, on_suspension):
        self.input = input
        self.output = output
        self.on_suspension = on_suspension

    def create_program(self, text, **kwargs):
        allocations, instructions = parser.parse("program", text)
        state = State(instructions, allocations)
        input = kwargs.get('input') or self.input
        output = kwargs.get('output') or self.output
        on_suspension = kwargs.get('on_suspension') or self.on_suspension
        io = IO(input, output)
        program = Program(state, io, on_suspension)
        return program

class Program(object):
    def __init__(self, state, io, on_suspension):
        self.state = state
        self.io = io
        self.on_suspension = on_suspension

    def execute(self):
        self.allocateMemory()
        self.execute_instructions()

    def allocateMemory(self):
        for a in self.state.allocations:
            a.allocate(self.state)

    def execute_instructions(self):
        while self.state.has_next_instruction():
            try:
                self.execute_next_instruction()
            except ProgramSuspension:
                self.on_suspension(self.state)
                break

    def execute_next_instruction(self):
        instruction = self.state.currentInstruction()
        if self.isLabel(instruction):
            self.state.increment_program_counter()
            self.execute_next_instruction()
        elif self.isBreak(instruction):
            self.state.increment_program_counter()
            self.suspendExecution()
        else:
#            logging.info("executing " + str(instruction))
#            logging.info(" of type " + str(type(instruction)))
            instruction.execute(self.adapt_io(self.io,self.state))
            self.state.increment_program_counter()
            # instructions rely on value of program_counter()
            # increment only after instruction.execute

    def suspendExecution(self):
        raise ProgramSuspension()

    def isLabel(self, instruction):
        return (type(instruction) is str) and (instruction != "BREAK")

    def isBreak(self, instruction):
        return instruction == "BREAK"

    def adapt_io(self, io, state):
        return IOState(io, state)

class IOState(object):
    def __init__(self, io, state):
        self.io = io
        self.state = state

    def _in(self): return self.io.input()
    def _out(self, val): self.io.output(val)

    def __getattr__(self, aname):
        f = getattr(self.state, aname)
        if isinstance(f, MethodType):
            return new.instancemethod(f.im_func, self, self.state.__class__)
        else:
            return f

class IO(object):
    def __init__(self, input, output):
        self.input = input
        self.output = output

class State(object):
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

        self.set_register("$ra", -1)
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

    def has_next_instruction(self):
        return self.program_counter() < len(self.instructions)

    def currentInstruction(self):
        return self.instructions[self.program_counter()]

    def program_counter(self):
        return self.registers["$pc"].value()

    def increment_program_counter(self):
        current_val = self.program_counter()
        self.set_register("$pc", current_val + 1)

    def set_register(self, reg, val):
        self.registers[reg].set_value(val)

    def register(self, reg):
        return self.registers[reg].value()
