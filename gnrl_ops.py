import logging
import copy

class JUMP(object):
    def __init__(self, label_ref):
        self.label_ref = label_ref

    def __str__(self):
        return "JUMP to " + self.label_ref

    def execute(self, state):
        return state.setRegister("$pc", state.instructions.index(self.label_ref))

class JAL(object):
    def __init__(self, label_ref):
        self.label_ref = label_ref

    def __str__(self):
        return "JAL to " + self.label_ref

    def execute(self, state):
        state = state.setRegister("$ra", state.programCounter())
        jump_position = state.instructions.index(self.label_ref)
        state = state.setRegister("$pc", jump_position)
        return state

class JR(object):
    def __init__(self, return_reg):
        self.return_reg = return_reg

    def __str__(self):
        return "JR " + self.return_reg

    def execute(self, state):
        jump_position = state.getRegister(self.return_reg)
        if jump_position != -1:
            return state.setRegister("$pc", jump_position)
        else:
            return state

class MFHI(object):
    def __init__(self, dst):
        self.dst = dst

    def __str__(self):
        return "MFHI " + self.dst

    def execute(self, state):
        val = state.getRegister("$hi")
        return state.setRegister(self.dst, val)

class MFLO(object):
    def __init__(self, dst):
        self.dst = dst

    def __str__(self):
        return "MFLO " + self.dst

    def execute(self, state):
        val = state.getRegister("$lo")
        return state.setRegister(self.dst, val)

class LW(object):
    def __init__(self, dst, indirect_address):
        self.dst = dst
        self.offset = indirect_address[0]
        self.base_register = indirect_address[1]

    def __str__(self):
        return "LW " + self.dst + " " + self.offset + " " + self.base_register

    def execute(self, state):
        state = copy.deepcopy(state)
        idx = -1
        base = state.getRegister(self.base_register)
        if type(self.offset) is str:
            idx = state.labels[self.offset] + (base / 4)
        else:
            idx = self.offset + (base / 4)
        state.setRegister(self.dst, state.memory[idx])
        return state

class SW(object):
    def __init__(self, src, indirect_address):
        self.src = src
        self.offset = indirect_address[0]
        self.base_register = indirect_address[1]

    def __str__(self):
        return "SW " + self.src  + " " + self.offset + " " + self.base_register

    def execute(self, state):
        state = copy.deepcopy(state)
        idx = -1
        base = state.getRegister(self.base_register)
        if type(self.offset) is str:
            idx = state.labels[self.offset] + (base / 4)
        else:
            idx = self.offset + (base / 4)
        val = state.getRegister(self.src)
        state.memory[idx] = val
        return state

class SYSCALL(object):
    def __init__(self): pass

    def __str__(self):
        return "SYSCALL"

    def execute(self, state):
        sysval = state.getRegister("$v0")
        return { 1 : self.print_integer,
                 2 : self.print_float,
                 3 : self.print_double,
                 4 : self.print_string,
                 5 : self.read_integer,
                 6 : self.read_float,
                 7 : self.read_double,
                 8 : self.read_string }[sysval](state)

    def print_integer(self, state):
        val = state.getRegister("$a0")
        state._out(val)
        return state

    def print_float(self, state):
        state._out(state.getRegiser("$f12"))
        return state

    def print_double(state):
        state._out(state.getRegister("$f12"))
        return state

    def print_string(self, state):
        idx = state.getRegister("$a0")
        val = ""
        for c in state.memory[idx:]:
            if not c is '\0':
                val += c
            else:
                break
        state._out(val)
        return state

    def read_integer(self, state):
        return state.setRegister("$v0", int(state._in()))

    def read_float(self, state):
        return state.setRegister("$f0", float(state._in()))

    def read_double(self, state):
        return state.setRegister("$f0", float(state._in()))

    def read_string(self, state):
        state = copy.deepcopy(state)
        x = state._in()
        idx = state.getRegister("$a0")
        length = state.getRegister("$a1")
        for i in range(0, min(length, len(x))):
            state.memory[idx + i] = x[i]
        state.memory[idx + min(length, len(x))] = "\0"
        return state

class CREATE_STRING(object):
    def __init__(self, label,  ascii_string):
        self.label = label
        self.ascii_string = ascii_string.replace('"', '') + "\0"

    def __str__(self):
        return "CREATE_STRING " + self.label + " " + self.ascii_string

    def allocate(self, state):
        state = copy.deepcopy(state)
        idx = len(state.memory)
        state.memory.extend(self.ascii_string)
        state.labels.update([[self.label, idx]])
        return state

class CREATE_SPACE(object):
    def __init__(self, label, size):
        self.label = label
        self.size = size

    def __str__(self):
        return "CREATE_SPACE " + self.label + " " + self.size

    def allocate(self, state):
        state = copy.deepcopy(state)
        if not (self.size % 4 == 0): raise "word addressing only at this time"

        array = map(lambda x : 0, range(0, self.size / 4))
        idx = len(state.memory)
        state.memory.extend(array)
        state.labels.update([[self.label, idx]])
        return state
