import new

def is_label(offset):
    return type(offset) is str

class Assignment(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return " ".join([self.__class__.name,
                         self.dst,
                         self.reg1,
                         self.reg2])

    def execute(self, state):
        val1 = state.register(self.reg1)
        val2 = state.register(self.reg2)
        result = self.operation(val1, val2)
        state.set_register(self.dst, result)


class AssignmentI(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def __str__(self):
        return " ".join([self.__class__.name,
                         self.dst,
                         self.reg,
                         self.im])

    def execute(self, state):
        val1 = state.register(self.reg)
        val2 = self.im
        result = self.operation(val1, val2)
        state.set_register(self.dst, result)

class AssignmentHiLo(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return " ".join([self.__class__.name,
                         self.reg1,
                         self.reg2])

    def execute(self, state):
        val1 = state.register(self.reg1)
        val2 = state.register(self.reg2)
        hi, lo = self.operation(val1, val2)
        state.set_register("$hi", hi)
        state.set_register("$lo", lo)

