import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='mipper.log',
                    filemode='w')

class Register:
    def __init__(self): self.value = 0

    def set_value(self, value): self.value = value

    def value(self): return self.value


class State:
    def create_registers(self, prefix, n):
        regs = []
        for i in range(0, n + 1):
            regs.append(prefix + str(i))
        return regs

    def __init__(self, instructions, allocations):
        self.position = 0
        regs = ["$gp", "$sp" "$fp", "$ra", "$zero", "$hi", "$lo"]
        regs.extend(self.create_registers("$v", 1))
        regs.extend(self.create_registers("$a", 3))
        regs.extend(self.create_registers("$t", 9))
        regs.extend(self.create_registers("$s", 7))
        regs.extend(self.create_registers("$k", 1))
        self.registers = dict(map(lambda reg: [reg, Register()], regs))
        self.instructions = instructions
        self.allocations = allocations

    def next(self):
        instruction = self.instructions[self.position]
        if not isinstance(instruction, str):
            self.instructions[self.position].execute(self)
        elif instruction == "syscall":
            self.system_call()
        self.position += 1

    def has_next(self): return self.position < len(self.instructions)

    def lookup_register(self, name):
        return self.registers[name]

    def set_register(self, name, value):
        logging.debug("setting " + name + " to " + str(value))
        self.registers[name].set_value(value)

    def system_call(self):
        sysval = self.registers["$v0"].value
        { 1 : self.print_integer,
          2 : self.print_float,
          3 : self.print_double,
          4 : self.print_string,
          5 : self.read_integer,
          6 : self.read_float,
          7 : self.read_double,
          8 : self.read_string }[sysval]()

    def print_integer(self):
        val = self.registers["$a0"].value
        print str(val),

    def print_float(self): pass
    def print_double(self): pass

    def print_string(self):
        val = self.registers["$a0"].value
        print str(val),

    def read_integer(self): pass
    def read_float(self): pass
    def read_double(self): pass
    def read_string(self): pass

