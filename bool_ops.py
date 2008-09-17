from mipper import AssignmentOp, AssignmentImmediate, AssignHiLo


def land(val1, val2):
    return val1 & val2
def lor(val1, val2):
    return val1 | val2
def slt(val1, val2):
    if val1 < val2:
        return 1
    else:
        return 0

class AND(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(land)

class OR(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(lor)

class ANDI(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    execute = AssignmentImmediate("dst", "reg", "im")(land)

class ORI(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    execute = AssignmentImmediate("dst", "reg", "im")(lor)

class Branch:
    def __init__(self, reg1, reg2, label_ref, test_fn):
        self.reg1 = reg1
        self.reg2 = reg2
        self.label_ref = label_ref
        self.test_fn = test_fn

    def execute(self, state):
        val1 = state.registers[self.reg1].getValue()
        val2 = state.registers[self.reg2].getValue()

        if self.test_fn(val1, val2):
            jump_position = state.instructions.index(self.label_ref)
            state.registers["$pc"].setValue(jump_position)

class BEQ(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x == y)

class BNE(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x != y)

class SLT(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg2
        self.reg2 = reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(slt)

class SLTI(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    execute = AssignmentImmediate("dst", "reg", "im")(slt)


class SLTU(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignmentOp("dst", "reg", "im")(slt)

class SLTIU(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    execute = AssignmentImmediate("dst", "reg", "im")(slt)
