import unittest
from mipper.mips import State
from mipper.ops.gnrl import *

class TestGeneralOperations(unittest.TestCase):
    def setUp(self):
        self.state = State(["a", "b", "c", "x", "y", "z"], [])
        self.state.memory.extend(range(0, 100))

    def testJUMP(self):
        op = JUMP("x")
        op.execute(self.state)
        result = self.state.programCounter()
        self.assertEqual(result, 3)

    def testJAL(self):
        prior_val = self.state.programCounter()
        op = JAL("c")
        op.execute(self.state)
        program_counter = self.state.programCounter()
        return_register = self.state.getRegister("$ra")
        self.assertEqual(program_counter, 2)
        self.assertEqual(return_register, prior_val)

    def testJR(self):
        self.state.setRegister("$ra", 44)
        op = JR("$ra")
        op.execute(self.state)
        self.assertEqual(self.state.programCounter(), 44)

    def testMFHI(self):
        self.state.setRegister("$hi", 22)
        op = MFHI("$t0")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 22)

    def testMFLO(self):
        self.state.setRegister("$lo", 88)
        op = MFLO("$t0")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 88)

    def testLW(self):
        op = LW("$t0", (1, "$zero"))
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 1)

    def testSW(self):
        self.state.setRegister("$t0", 22)
        op = SW("$t0", (2, "$zero"))
        op.execute(self.state)
        result = self.state.memory[2]
        self.assertEqual(result, 22)


if __name__ == '__main__':
    unittest.main()

