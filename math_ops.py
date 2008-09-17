def checkOverflow(val):
    if type(val) is long:
        raise "overflow exception"

class ADD:
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].getValue()
        result = val1 + val2
        checkOverflow(result)
        state.registers[self.dst].setValue(result)

class SUB:
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].setValue()
        result = val1 - val2
        checkOverflow(result)
        state.registers[self.dst].setValue(result)

class ADDU:
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].getValue()
        state.registers[self.dst].setValue(val1 + val2)

class ADDI:
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def execute(self, state):
        val = state.registers[self.reg].getValue()
        result = val + self.im
        checkOverflow(result)
        state.registers[self.dst].setValue(val + self.im)

class ADDIU:
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def execute(self, state):
        val = state.registers[self.reg].getValue()
        state.registers[self.dst].setValue(val + self.im)

class SUBU:
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].getValue()
        state.registers[self.dst].setValue(val1 - val2)

class DIV:
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].getValue()
        hi = val1 % val2
        lo = val1 / val2
        state.registers["$hi"].setValue(hi)
        state.registers["$lo"].setValue(lo)

class DIVU:
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].getValue()
        hi = val1 % val2
        lo = val1 / val2
        state.registers["$hi"].setValue(hi)
        state.registers["$lo"].setValue(lo)

class MULT:
    def __init__(self, reg1,reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].getValue()
        result = val1 * val2
        if type(result) is long:
            hi = result >> 32
            lo = result & 0x7FFFFFFF
        else:
            hi = 0
            lo = result
        state.registers["$hi"] = hi
        state.registers["$lo"] = lo



