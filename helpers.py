
def AssignmentOp(dst, reg1, reg2):
    def f(meth):
        def g(obj, state):
            val1 = state.registers[obj.__getattribute__(reg1)].getValue()
            val2 = state.registers[obj.__getattribute__(reg2)].getValue()
            result = meth(val1, val2)
            state.registers[obj.__getattribute__(dst)].setValue(result)
        return g
    return f

def AssignmentImmediate(dst, reg1, im):
    def f(meth):
        def g(obj, state):
            val1 = state.registers[obj.__getattribute__(reg1)].getValue()
            val2 = obj.__getattribute__(im)
            result = meth(val1, val2)
            state.registers[obj.__getattribute__(dst)].setValue(result)
        return g
    return f

def AssignHiLo(reg1, reg2):
    def f(meth):
        def g(obj, state):
            val1 = state.registers[obj.__getattribute__(reg1)].getValue()
            val2 = state.registers[obj.__getattribute__(reg2)].getValue()
            hi, lo = meth(val1, val2)
            state.registers["$hi"].setValue(hi)
            state.registers["$lo"].setValue(lo)
        return g
    return f
