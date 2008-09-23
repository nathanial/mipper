from Mipper.helpers import AssignmentOp, AssignmentImmediate, AssignHiLo

class OverflowException: pass

max_int = 2147483647

def checkOverflow(val):
    if type(val) is long:
        raise OverflowException()

def checked(meth):
    def f(val1, val2):
        result = meth(val1, val2)
        checkOverflow(result)
        return result
    return f

def unchecked(meth):
    def f(val1, val2):
        result = meth(val1, val2)
        try:
            checkOverflow(result)
        except OverflowException:
            overflow = result % max_int
            if result > 0:
                result = overflow - max_int - 2
            else:
                result = overflow + max_int + 2
            result = result.__int__()
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

    def __str__(self):
        return "ADD " + self.dst + " " + self.reg1 + " " + self.reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(checked(add))

class SUB(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return "SUB " + self.dst + " " + self.reg1 + " " + self.reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(checked(sub))

class ADDU(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return "ADDU " + self.dst + " " + self.reg1 + " " + self.reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(unchecked(add))

class ADDI(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def __str__(self):
        return "ADDI " + self.dst + " " + self.reg + " " + str(self.im)

    execute = AssignmentImmediate("dst", "reg", "im")(checked(add))

class ADDIU(object):
    def __init__(self, dst, reg, im):
        self.dst = dst
        self.reg = reg
        self.im = im

    def __str__(self):
        return "ADDIU " + self.dst + " " + self.reg + " " + str(self.im)

    execute = AssignmentImmediate("dst", "reg", "im")(unchecked(add))

class SUBU(object):
    def __init__(self, dst, reg1, reg2):
        self.dst = dst
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return "SUBU " + self.dst + " " + self.reg1 + " " + self.reg2

    execute = AssignmentOp("dst", "reg1", "reg2")(unchecked(sub))

class DIV(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return "DIV " + self.reg1 + " " + self.reg2

    execute = AssignHiLo("reg1", "reg2")(unchecked(div))

class DIVU(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return "DIVU " + self.reg1 + " " + self.reg2

    execute = AssignHiLo("reg1", "reg2")(unchecked(div))

class MULT(object):
    def __init__(self, reg1,reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return "MULT " + self.reg1 + " " + self.reg2

    execute = AssignHiLo("reg1", "reg2")(unchecked(mult))



