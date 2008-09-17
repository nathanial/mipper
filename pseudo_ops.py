from bool_ops import Branch
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s %(message)s",
                    filename="ops.log")

class LA:
    def __init__(self, dst, label_ref):
        self.dst = dst
        self.label_ref = label_ref

    def execute(self, state):
        idx = state.labels[self.label_ref]
        state.registers[self.dst].setValue(idx)

class LI:
    def __init__(self, dst, im):
        self.dst = dst
        self.im = im

    def execute(self, state):
        state.registers[self.dst].setValue(self.im)

class MOVE:
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def execute(self, state):
        state.registers[self.dst].setValue(
            state.registers[self.src].getValue())

class BGT(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x > y)

class BLT(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x < y)

class BGE(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x >= y)

class BLE(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x <= y)

class BGTU(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x > y)

class BGTZ(Branch):
    def __init__(self, reg1, label_ref):
        Branch.__init__(self, reg1, "$zero", label_ref, lambda x,y: x > y)

