from mipper.helpers import Assignment, AssignmentI, AssignmentHiLo

class MipsOverflowException: pass

max_int = 2147483647

def checkOverflow(val):
    if type(val) is long:
        raise MipsOverflowException()

def checked(meth):
    def h(obj, val1, val2):
        result = meth(val1, val2)
        checkOverflow(result)
        return result
    return h

def unchecked(meth):
    def h(obj, val1, val2):
        result = meth(val1, val2)
        try:
            checkOverflow(result)
        except MipsOverflowException:
            overflow = result % max_int
            if result > 0:
                result = overflow - max_int - 2
            else:
                result = overflow + max_int + 2
            result = result.__int__()
        return result
    return h

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

class ADD(Assignment):
    name =  "ADD"
    operation = checked(add)

class SUB(Assignment):
    name = "SUB"
    operation = checked(sub)

class ADDU(Assignment):
    name = "ADDU"
    operation = unchecked(add)

class ADDI(AssignmentI):
    name = "ADDI"
    operation = checked(add)

class ADDIU(AssignmentI):
    name = "ADDIU"
    operation = unchecked(add)

class SUBU(Assignment):
    name = "SUBU"
    operation = unchecked(sub)

class DIV(AssignmentHiLo):
    name = "DIV"
    operation = unchecked(div)

class DIVU(AssignmentHiLo):
    name = "DIVU"
    operation = unchecked(div)

class MULT(AssignmentHiLo):
    name = "MULT"
    operation = unchecked(mult)



