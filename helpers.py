
def AssignmentOp(dst, reg1, reg2):
    def f(meth):
        def g(obj, program):
            val1 = program.register(obj.__getattribute__(reg1))
            val2 = program.register(obj.__getattribute__(reg2))
            result = meth(val1, val2)
            program.set_register(obj.__getattribute__(dst), result)
        return g
    return f

def AssignmentImmediate(dst, reg1, im):
    def f(meth):
        def g(obj, program):
            val1 = program.register(obj.__getattribute__(reg1))
            val2 = obj.__getattribute__(im)
            result = meth(val1, val2)
            program.set_register(obj.__getattribute__(dst), result)
        return g
    return f

def AssignHiLo(reg1, reg2):
    def f(meth):
        def g(obj, program):
            val1 = program.register(obj.__getattribute__(reg1))
            val2 = program.register(obj.__getattribute__(reg2))
            hi, lo = meth(val1, val2)
            program.set_register("$hi", hi)
            program.set_register("$lo", lo)
        return g
    return f
