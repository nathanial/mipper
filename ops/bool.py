from mipper.helpers import Assignment, AssignmentI, AssignmentHiLo


def land(obj, val1, val2):
    return val1 & val2
def lor(obj, val1, val2):
    return val1 | val2
def slt(obj, val1, val2):
    if val1 < val2:
        return 1
    else:
        return 0

class AND(Assignment):
    name = "AND"
    operation = land

class OR(Assignment):
    name = "OR"
    operation = lor

class ANDI(AssignmentI):
    name = "ANDI"
    operation = land

class ORI(AssignmentI):
    name = "ORI"
    operation = lor

class Branch:
    def __init__(self, reg1, reg2, label_ref):
        self.reg1 = reg1
        self.reg2 = reg2
        self.label_ref = label_ref

    def execute(self, state):
        val1 = state.register(self.reg1)
        val2 = state.register(self.reg2)

        if self.test(val1, val2):
            jump_position = state.instructions.index(self.label_ref)
            state.set_register("$pc", jump_position)

class BEQ(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref)

    def test(self, x, y):
        return x == y

    def __str__(self):
        return "BEQ " + self.reg1 + " " + self.reg2 + " " + self.label_ref

class BNE(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref)

    def test(self, x, y):
        return x != y

    def __str__(self):
        return "BNE " + self.reg1 + " " + self.reg2 + " " + self.label_ref

class SLT(Assignment):
    name = "SLT"
    operation = slt

class SLTI(AssignmentI):
    name = "SLTI"
    operation = slt

class SLTU(Assignment):
    name = "SLTU"
    operation = slt

class SLTIU(AssignmentI):
    name = "SLTIU"
    operation = slt
