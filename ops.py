import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='mipper.log',
                    filemode='w')

class ADD:
    def __init__(self, destination, reg1, reg2):
        self.destination = destination
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        logging.debug("ADD " + self.destination + " " +
                      self.reg1 + " " + self.reg2)

        val1 = state.lookup_register(self.reg1).value
        val2 = state.lookup_register(self.reg2).value
        state.set_register(self.destination, val1 + val2)

class ADDI:
    def __init__(self, destination, reg1, i2):
        self.destination = destination
        self.reg1 = reg1
        self.i2 = i2

    def execute(self, state):
        logging.debug("ADDI " + self.destination + " " +
                      self.reg1 + " " + str(self.i2))

        val1 = state.lookup_register(self.reg1).value
        state.set_register(self.destination, val1 + self.i2)

class LI:
    def __init__(self, destination, immediate):
        self.destination = destination
        self.immediate = immediate

    def execute(self, state):
        logging.debug("LI " + self.destination + " " + str(self.immediate))
        state.set_register(self.destination, self.immediate)

class JUMP:
    def __init__(self, label_ref):
        self.label_ref = label_ref

    def execute(self, state):
        logging.debug("JUMP to " + self.label_ref)
        position = state.instructions.index(self.label_ref)
        state.position = position

class JAL:
    def __init__(self, label_ref):
        self.label_ref = label_ref

    def execute(self, state):
        logging.debug("JAL to " + self.label_ref)
        jump_position = state.instructions.index(self.label_ref)
        state.set_register("$ra", state.position)
        state.position = jump_position

class JR:
    def __init__(self, return_reg):
        self.return_reg = return_reg

    def execute(self, state):
        logging.debug("JR to " + self.return_reg)
        state.position = state.lookup_register(self.return_reg).value

class Branch:
    def __init__(self, reg1, reg2, label_ref, test_fn):
        self.reg1 = reg1
        self.reg2 = reg2
        self.label_ref = label_ref
        self.test_fn = test_fn

    def execute(self, state):
        logging.debug("Branch " + self.reg1 + " " +
                      self.reg2 + " " + self.label_ref)
        val1 = state.lookup_register(self.reg1).value
        val2 = state.lookup_register(self.reg2).value

        if self.test_fn(val1, val2):
            logging.debug("Jumping to " + self.label_ref)
            position = state.instructions.index(self.label_ref)
            state.position = position

class BEQ(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x == y)

class BNE(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x != y)

class BLT(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x < y)

class BGT(Branch):
    def __init__(self, reg1, reg2, label_ref):
        Branch.__init__(self, reg1, reg2, label_ref, lambda x,y: x > y)

class LA:
    def __init__(self, dst, address):
        self.dst = dst
        self.address = address

    def execute(self, state):
        logging.debug("LA " + self.dst + " " + self.address)
        val = state.allocations[self.address]
        state.set_register(self.dst, val)

class MOVE:
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def execute(self, state):
        logging.debug("MOVE " + self.dst + " " + self.src)
        val = state.lookup_register(self.src).value
        state.set_register(self.dst, val)

class DIV:
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def execute(self, state):
        logging.debug("DIV " + self.reg1 + " " + self.reg2)
        val1 = state.lookup_register(self.reg1).value
        val2 = state.lookup_register(self.reg2).value
        hi = val1 % val2
        lo = val1 / val2
        state.set_register("$hi", hi)
        state.set_register("$lo", lo)

class MFHI:
    def __init__(self, dst):
        self.dst = dst

    def execute(self, state):
        logging.debug("MFHI " + self.dst)
        val = state.lookup_register("$hi").value
        state.set_register(self.dst, val)
