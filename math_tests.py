import unittest
from Mipper.mipper import State
from Mipper.math_ops import *


class TestMathOperations(unittest.TestCase):
    def setUp(self):
        self.t0 = 0
        self.t1 = 10
        self.t2 = 88

        self.state = State([], []).setRegister("$t0", self.t0).setRegister("$t1", self.t1).setRegister("$t2", self.t2)

    def testADD(self):
        op = ADD("$t0", "$t1", "$t2")
        state = op.execute(self.state)
        result = state.getRegister("$t0")
        self.assertEqual(result, self.t1 + self.t2)

    def testSUB(self):
        op = SUB("$t0", "$t1", "$t2")
        state = op.execute(self.state)
        result = state.getRegister("$t0")
        self.assertEqual(result, self.t1 - self.t2)

    def testADDU(self):
        op = ADDU("$t0", "$t1", "$t2")
        state = op.execute(self.state)
        result = state.getRegister("$t0")
        self.assertEqual(result, self.t1 + self.t2)

    def testADDI(self):
        op = ADDI("$t0", "$t1", 22)
        state = op.execute(self.state)
        result = state.getRegister("$t0")
        self.assertEqual(result, self.t1 + 22)

    def testADDIU(self):
        op = ADDIU("$t0", "$t1", 22)
        state = op.execute(self.state)
        result = state.getRegister("$t0")
        self.assertEqual(result, self.t1 + 22)

    def testSUBU(self):
        op = SUBU("$t0", "$t1", "$t2")
        state = op.execute(self.state)
        result = state.getRegister("$t0")
        self.assertEqual(result, self.t1 - self.t2)

    def testDIV(self):
        op = DIV("$t1", "$t2")
        state = op.execute(self.state)
        hi = state.getRegister("$hi")
        lo = state.getRegister("$lo")
        self.assertEqual(hi, self.t1 % self.t2)
        self.assertEqual(lo, self.t1 / self.t2)

    def testDIVU(self):
        op = DIVU("$t1", "$t2")
        state = op.execute(self.state)
        hi = state.getRegister("$hi")
        lo = state.getRegister("$lo")
        self.assertEqual(hi, self.t1 % self.t2)
        self.assertEqual(lo, self.t1 / self.t2)

    def testMULT(self):
        op = MULT("$t1", "$t2")
        state = op.execute(self.state)
        hi = state.getRegister("$hi")
        lo = state.getRegister("$lo")
        self.assertEqual(hi, 0)
        self.assertEqual(lo, self.t1 * self.t2)

if __name__ == '__main__':
    unittest.main()
