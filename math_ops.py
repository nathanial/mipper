from Mipper.helpers import AssignmentOp, AssignmentImmediate, AssignHiLo

def checkOverflow(val):
    if type(val) is long:
        raise "overflow exception"

def checked(meth):
    def f(val1, val2):
        result = meth(val1, val2)
        checkOverflow(result)
        return result
    return f

def add(val1, val2): return val1 + val2
def sub(val1, val2): return val1 - val2
def div(val1, val2): return (val1 % val2, val1 / val2)
def mult(val1, val2):
    result = val1 * val2
    if type(result) is long:
        hi = result >> 32
        lo = result & 0x7FFFFFFF
    else:
        hi = 0
        lo = result
    return hi, lo

class ADD(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(checked(add))

class SUB(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(checked(sub))

class ADDU(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(add)

class ADDI(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    execute = AssignmentImmediate("dst", "reg", "im")(checked(add))

class ADDIU(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    execute = AssignmentImmediate("dst", "reg", "im")(add)

class SUBU(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(sub)

class DIV(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignHiLo("reg1", "reg2")(div)

class DIVU(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignHiLo("reg1", "reg2")(div)

class MULT:
    def __init__(self, reg1,reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    execute = AssignHiLo("reg1", "reg2")(mult)



