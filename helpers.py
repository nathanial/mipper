
def AssignmentOp(dst, reg1, reg2):
    def f(meth):
        def g(obj, state):
            val1 = state.getRegister(obj.__getattribute__(reg1))
            val2 = state.getRegister(obj.__getattribute__(reg2))
            result = meth(val1, val2)
            state.setRegister(obj.__getattribute__(dst), result)
        return g
    return f

def AssignmentImmediate(dst, reg1, im):
    def f(meth):
        def g(obj, state):
            val1 = state.getRegister(obj.__getattribute__(reg1))
            val2 = obj.__getattribute__(im)
            result = meth(val1, val2)
            state.setRegister(obj.__getattribute__(dst), result)
        return g
    return f

def AssignHiLo(reg1, reg2):
    def f(meth):
        def g(obj, state):
            val1 = state.getRegister(obj.__getattribute__(reg1))
            val2 = state.getRegister(obj.__getattribute__(reg2))
            hi, lo = meth(val1, val2)
            state.setRegister("$hi", hi)
            state.setRegister("$lo", lo)
        return g
    return f
