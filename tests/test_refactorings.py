from mipper.mips import State
from mipper.ops.math import ADD

def test():
    state = State([],[])
    state.set_register("$t1", 1)
    state.set_register("$t2", 2)
    add = ADD("$t0", "$t1", "$t2")
    add.execute(state)
    print state.register("$t0")

if __name__ == "__main__":
    test()
