from Mipper.helpers import AssignmentOp, AssignmentImmediate, AssignHiLo


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

    def __str__(self):
        return "AND " + self.dst + " " + self.reg1 + " " + self.reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(land)

class OR(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return "OR " + self.dst + " " + self.reg1 + " " + self.reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(lor)

class ANDI(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def __str__(self):
        return "ANDI " + self.dst + " " + self.reg + " " + str(self.im)

    execute = AssignmentImmediate("dst", "reg", "im")(land)

class ORI(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def __str__(self):
        return "ORI " + self.dst + " " + self.reg + " " + str(self.im)

    execute = AssignmentImmediate("dst", "reg", "im")(lor)

class Branch:
    def __init__(self, reg1, reg2, label_ref, test_fn):
        self.reg1 = reg1
        self.reg2 = reg2
        self.label_ref = label_ref
        self.test_fn = test_fn

    def execute(self, state):
        val1 = state.getRegister(self.reg1)
        val2 = state.getRegister(self.reg2)

        if self.test_fn(val1, val2):
            jump_position = state.instructions.index(self.label_ref)
            state.setRegister("$pc", jump_position)

class BEQ(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x == y)

    def __str__(self):
        return "BEQ " + self.reg1 + " " + self.reg2 + " " + self.label_ref

class BNE(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x != y)

    def __str__(self):
        return "BNE " + self.reg1 + " " + self.reg2 + " " + self.label_ref

class SLT(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg2
        self.reg2 = reg2

    def __str__(self):
        return "SLT " + self.dst + " " + self.reg1 + " " + self.reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(slt)

class SLTI(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def __str__(self):
        return "SLTI " + self.dst + " " + self.dst + " " + self.reg + " " + self.im

    execute = AssignmentImmediate("dst", "reg", "im")(slt)


class SLTU(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return "SLTU " + self.dst + " " + self.reg1 + " " + self.reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(slt)

class SLTIU(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def __str__(self):
        return "SLTIU " + self.dst + " " + self.reg + " " + self.im

    execute = AssignmentImmediate("dst", "reg", "im")(slt)
