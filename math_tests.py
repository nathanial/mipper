import unittest
from Mipper.mipper import State
from Mipper.math_ops import *

class TestMathOperations(unittest.TestCase):
    def setUp(self):
        self.state = State([], [])
        self.t0 = 0
        self.t1 = 10
        self.t2 = 88
        self.state.registers["$t0"].setValue(self.t0)
        self.state.registers["$t1"].setValue(self.t1)
        self.state.registers["$t2"].setValue(self.t2)

    def testADD(self):
        op = ADD("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.registers["$t0"].getValue()
        self.assertEqual(result, self.t1 + self.t2)

    def testSUB(self):
        op = SUB("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.registers["$t0"].getValue()
        self.assertEqual(result, self.t1 - self.t2)

    def testADDU(self):
        op = ADDU("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.registers["$t0"].getValue()
        self.assertEqual(result, self.t1 + self.t2)

    def testADDI(self):
        op = ADDI("$t0", "$t1", 22)
        op.execute(self.state)
        result = self.state.registers["$t0"].getValue()
        self.assertEqual(result, self.t1 + 22)

    def testADDIU(self):
        op = ADDIU("$t0", "$t1", 22)
        op.execute(self.state)
        result = self.state.registers["$t0"].getValue()
        self.assertEqual(result, self.t1 + 22)

    def testSUBU(self):
        op = SUBU("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.registers["$t0"].getValue()
        self.assertEqual(result, self.t1 - self.t2)

    def testDIV(self):
        op = DIV("$t1", "$t2")
        op.execute(self.state)
        hi = self.state.registers["$hi"].getValue()
        lo = self.state.registers["$lo"].getValue()
        self.assertEqual(hi, self.t1 % self.t2)
        self.assertEqual(lo, self.t1 / self.t2)

    def testDIVU(self):
        op = DIVU("$t1", "$t2")
        op.execute(self.state)
        hi = self.state.registers["$hi"].getValue()
        lo = self.state.registers["$lo"].getValue()
        self.assertEqual(hi, self.t1 % self.t2)
        self.assertEqual(lo, self.t1 / self.t2)

    def testMULT(self):
        op = MULT("$t1", "$t2")
        op.execute(self.state)
        hi = self.state.registers["$hi"].getValue()
        lo = self.state.registers["$lo"].getValue()
        self.assertEqual(hi, 0)
        self.assertEqual(lo, self.t1 * self.t2)

if __name__ == '__main__':
    unittest.main()
