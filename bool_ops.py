class AND:
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].getValue()
        result = val1 & val2
        state.registers[self.dst].setValue(result)

class OR:
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].getValue()
        result = val1 | val2
        state.registers[self.dst].setValue(result)

class ANDI:
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def execute(self, state):
        val = state.registers[self.reg].getValue()
        result = val & self.im
        state.registers[self.dst].setValue(result)

class ORI:
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def execute(self, state):
        val = state.registers[self.reg].getValue()
        result = val | self.im
        state.registers[self.dst].setValue(result)

class Branch:
    def __init__(self, reg1, reg2, label_ref, test_fn):
        self.reg1 = reg1
        self.reg2 = reg2
        self.label_ref = label_ref
        self.test_fn = test_fn

    def execute(self, state):
        val1 = state.registers[reg1].getValue()
        val2 = state.registers[reg2].getValue()

        if self.test_fn(val1, val2):
            jump_position = state.instructions.index(self.label_ref)
            state.registers["$pc"].setValue(jump_position)

class BEQ(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x == y)

class BNE(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x != y)
