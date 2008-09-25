import unittest
from mipper.mips import State
from mipper.ops.bool import *

class TestBoolOperations(unittest.TestCase):
    def setUp(self):
        self.state = State([], [])
        self.branch_state = State(["x", "y", "z", "BLAH", "LOOP"], [])

        self.t0 = 0
        self.t1 = 434
        self.t2 = 0

        self.state.setRegister("$t0", self.t0)
        self.state.setRegister("$t1", self.t1)
        self.state.setRegister("$t2", self.t2)

        self.branch_state.setRegister("$t0", self.t0)
        self.branch_state.setRegister("$t1", self.t1)
        self.branch_state.setRegister("$t2", self.t2)

    def testAND(self):
        op = AND("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 0)

    def testOR(self):
        op = OR("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 434)

    def testANDI(self):
        op = ANDI("$t0", "$t1", 434)
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 434)

    def testORI(self):
        op = ORI("$t0", "$t1", 0)
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 434)

    def testBEQ(self):
        prior_val = self.branch_state.programCounter()
        op = BEQ("$t1", "$t2", "LOOP")
        op.execute(self.branch_state)
        result = self.branch_state.programCounter()
        self.assertEqual(result, prior_val)
        self.branch_state.setRegister("$pc", 0)

    def testBNE(self):
        prior_val = self.branch_state.programCounter()
        op = BNE("$t1", "$t2", "LOOP")
        op.execute(self.branch_state)
        result = self.branch_state.programCounter()
        self.assertEqual(result, 4)
        self.branch_state.setRegister("$pc", 0)

    def testSLT(self):
        op = SLT("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 0)

    def testSLTI(self):
        op = SLTI("$t0", "$t2", 1)
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 1)

    def testSLTU(self):
        op = SLTU("$t0", "$t1", "$t2")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 0)

    def testSLTIU(self):
        op = SLTIU("$t0", "$t1", 0)
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
