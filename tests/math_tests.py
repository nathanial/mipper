import unittest
from mipper.mips import State
from mipper.ops.math import *

max_int = 2147483647

class TestMathOperations(unittest.TestCase):
    def setUp(self):
        self.state = State([], [])
        self.t0 = 0
        self.t1 = 10
        self.t2 = 88
        self.t3 = max_int
        self.t4 = 22
        self.state.setRegister("$t0", self.t0)
        self.state.setRegister("$t1", self.t1)
        self.state.setRegister("$t2", self.t2)
        self.state.setRegister("$t3", self.t3)
        self.state.setRegister("$t4", self.t4)

    def testADD(self):
        op = ADD("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, self.t1 + self.t2)

    def testSUB(self):
        op = SUB("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, self.t1 - self.t2)

    def testADDU(self):
        op = ADDU("$t0", "$t3", "$t4")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, -2147483627)

    def testADDI(self):
        op = ADDI("$t0", "$t1", 22)
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, self.t1 + 22)

    def testADDIU(self):
        op = ADDIU("$t0", "$t3", 22)
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, -2147483627)

    def testSUBU(self):
        op = SUBU("$t0", "$t4", "$t3")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, -2147483625)

    def testDIV(self):
        op = DIV("$t1", "$t2")
        op.execute(self.state)
        hi = self.state.getRegister("$hi")
        lo = self.state.getRegister("$lo")
        self.assertEqual(hi, self.t1 % self.t2)
        self.assertEqual(lo, self.t1 / self.t2)

    def testDIVU(self):
        op = DIVU("$t1", "$t2")
        op.execute(self.state)
        hi = self.state.getRegister("$hi")
        lo = self.state.getRegister("$lo")
        self.assertEqual(hi, self.t1 % self.t2)
        self.assertEqual(lo, self.t1 / self.t2)

    def testMULT(self):
        op = MULT("$t1", "$t2")
        op.execute(self.state)
        hi = self.state.getRegister("$hi")
        lo = self.state.getRegister("$lo")
        self.assertEqual(hi, 0)
        self.assertEqual(lo, self.t1 * self.t2)

if __name__ == '__main__':
    unittest.main()
