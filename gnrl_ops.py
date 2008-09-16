class JUMP:
    def __init__(self, label_ref):
        self.label_ref = label_ref

    def execute(self, state):
        state.registers["$pc"].setValue(state.instructions.index(self.label_ref))

class JAL:
    def __init__(self, label_ref):
        self.label_ref = label_ref

    def execute(self, state):
        state.registers["$ra"].setValue(state.currentInstruction() + 1)
        jump_position = state.instructions.index(self.label_ref)
        state.registers["$pc"].setValue(jump_position)

class JR:
    def __init__(self, return_reg):
        self.return_reg = return_reg

    def execute(self, state):
        jump_position = state.registers[self.return_reg].getValue()
        state.registers["$pc"].setValue(jump_position)



class MFHI:
    def __init__(self, dst):
        self.dst = dst

    def execute(self, state):
        logging.debug("MFHI " + self.dst)
        val = state.lookup_register("$hi").value
        state.set_register(self.dst, val)

class CREATE_STRING:
    def __init__(self, label,  ascii_string):
        self.label = label
        self.ascii_string = ascii_string.replace('"', '')

    def allocate(self, state):
        state.allocations.update([[self.label, self.ascii_string]])

class CREATE_SPACE:
    def __init__(self, label, size):
        self.label = label
        self.size = size

    def allocate(self, state):
        array = map(lambda x : 0, range(0, self.size))
        state.allocations.update([[self.label, array]])

class LW:
    def __init__(self, dst, indirect_address):
        self.dst = dst
        self.offset = indirect_address[0]
        self.base_register = indirect_address[1]

    def execute(self, state):
        if isinstance(self.offset, str):
            alloc = state.allocations[self.offset]
            base = state.lookup_register(self.base_register).value
            if not base % 4 == 0: raise "only word address permitted"
            else:
                value = alloc[base / 4]
                state.set_register(self.dst, value)

        else:
            raise "unsupported operation: numerical index"

class SW:
    def __init__(self, src, indirect_address):
        self.src = src
        self.offset = indirect_address[0]
        self.base_register = indirect_address[1]

    def execute(self, state):
        if isinstance(self.offset, str):
            alloc = state.allocations[self.offset]
            base = state.lookup_register(self.base_register).value
            if not base % 4 == 0: raise "only word addresses permitted"
            else:
                value = state.lookup_register(self.src).value
                alloc[base / 4] = value
        else:
            raise "unsupported operation: numerical index"

class SYSCALL:
    def __init__(self): pass

    def execute(self, state):
        sysval = state.registers["$v0"].value
        { 1 : self.print_integer,
          2 : self.print_float,
          3 : self.print_double,
          4 : self.print_string,
          5 : self.read_integer,
          6 : self.read_float,
          7 : self.read_double,
          8 : self.read_string }[sysval](state)

    def print_integer(state):
        val = state.registers["$a0"].value
        print str(val),

    def print_float(self): pass
    def print_double(self): pass

    def print_string(self):
        val = state.registers["$a0"].value
        print str(val),

    def read_integer(self): pass
    def read_float(self): pass
    def read_double(self): pass
    def read_string(self): pass