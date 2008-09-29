from bool import Branch
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s %(message)s",
                    filename="ops.log")

class LA:
    def __init__(self, dst, label_ref):
        self.dst = dst
        self.label_ref = label_ref

    def __str__(self):
        return "LA " + self.dst + " " + self.label_ref

    def execute(self, state):
        idx = state.labels[self.label_ref]
        state.set_register(self.dst, idx)

class LI:
    def __init__(self, dst, im):
        self.dst = dst
        self.im = im

    def __str__(self):
        return "LI " + self.dst + " " + str(self.im)

    def execute(self, state):
        state.set_register(self.dst, self.im)

class MOVE:
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __str__(self):
        return "MOVE " + self.dst + " " + self.src

    def execute(self, state):
        state.set_register(self.dst, state.register(self.src))

class BGT(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref)

    def test(self, x, y):
        return x > y

    def __str__(self):
        return "BGT " + self.reg1 + " " + self.reg2 + " " + self.label_ref

class BLT(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref)

    def test(self, x, y):
        return x < y

    def __str__(self):
        return "BLT " + self.reg1 + " " + self.reg2 + " " + self.label_ref

class BGE(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref)

    def test(self, x, y):
        return x >= y

    def __str__(self):
        return "BGE " + self.reg1 + " " + self.reg2 + " " + self.label_ref

class BLE(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref)

    def test(self, x, y):
        return x <= y

    def __str__(self):
        return "BLE " + self.reg1 + " " + self.reg2 + " " + self.label_ref

class BGTU(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref)

    def test(self, x, y):
        return x > y

    def __str__(self):
        return "BGTU " + self.reg1 + " " + self.reg2 + " " + self.label_ref

class BGTZ(Branch):
    def __init__(self, reg1, label_ref):
        Branch.__init__(self, reg1, "$zero", label_ref)

    def test(self, x, y):
        return x > y

    def __str__(self):
        return "BGTZ " + self.reg1 + " " + self.label_ref
