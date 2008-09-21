import unittest
from Mipper.mipper import State
from Mipper.pseudo_ops import *

class TestPseudoOperations(unittest.TestCase):
    def setUp(self):
        self.state = State([], [])
        self.t0 = 17
        self.t1 = 100
        self.state.registers["$t0"].setValue(self.t0)
        self.state.registers["$t1"].setValue(self.t1)
        self.state.labels = {"x": 0, "y": 1, "z": 2, "a": 3, "b": 4}

        self.branch_state = State(["a", "b", "c", "d"], [])
        self.branch_state.registers["$t0"].setValue(1)
        self.branch_state.registers["$t1"].setValue(11)

    def testLA(self):
        op = LA("$t0", "a")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 3)

    def testLI(self):
        op = LI("$t0", 23)
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 23)

    def testMOVE(self):
        op = MOVE("$t0", "$t1")
        op.execute(self.state)
        result = self.state.getRegister("$t0")
        self.assertEqual(result, 100)

    def testBGT(self):
        prior_val = self.branch_state.programCounter()
        op = BGT("$t0", "$t1", "d")
        op.execute(self.branch_state)
        result = self.branch_state.programCounter()
        self.assertEqual(result, prior_val)

    def testBLT(self):
        op = BLT("$t0", "$t1", "c")
        op.execute(self.branch_state)
        result = self.branch_state.programCounter()
        self.assertEqual(result, 2)

    def testBGE(self):
        prior_val = self.branch_state.programCounter()
        op = BGE("$t0", "$t1", "b")
        op.execute(self.branch_state)
        result = self.branch_state.programCounter()
        self.assertEqual(result, prior_val)

    def testBLE(self):
        op = BLE("$t0", "$t1", "b")
        op.execute(self.branch_state)
        result = self.branch_state.programCounter()
        self.assertEqual(result, 1)

    def testBGTU(self):
        prior_val = self.branch_state.programCounter()
        op = BGTU("$t0", "$t1", "b")
        op.execute(self.branch_state)
        result = self.branch_state.programCounter()
        self.assertEqual(result, prior_val)

    def testBGTZ(self):
        op = BGTZ("$t0", "c")
        op.execute(self.branch_state)
        result = self.branch_state.programCounter()
        self.assertEqual(result, 2)

if __name__ == "__main__":
    unittest.main()