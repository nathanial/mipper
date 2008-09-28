import unittest
from mipper.mips import State
from mipper.ops.pseudo import *

class TestPseudoOperations(unittest.TestCase):
    def setUp(self):
        self.state = State([], [])
        self.t0 = 17
        self.t1 = 100
        self.state.set_register("$t0", self.t0)
        self.state.set_register("$t1", self.t1)
        self.state.labels = {"x": 0, "y": 1, "z": 2, "a": 3, "b": 4}

        self.branch_state = State(["a", "b", "c", "d"], [])
        self.branch_state.set_register("$t0", 1)
        self.branch_state.set_register("$t1", 11)

    def testLA(self):
        op = LA("$t0", "a")
        op.execute(self.state)
        result = self.state.register("$t0")
        self.assertEqual(result, 3)

    def testLI(self):
        op = LI("$t0", 23)
        op.execute(self.state)
        result = self.state.register("$t0")
        self.assertEqual(result, 23)

    def testMOVE(self):
        op = MOVE("$t0", "$t1")
        op.execute(self.state)
        result = self.state.register("$t0")
        self.assertEqual(result, 100)

    def testBGT(self):
        prior_val = self.branch_state.program_counter()
        op = BGT("$t0", "$t1", "d")
        op.execute(self.branch_state)
        result = self.branch_state.program_counter()
        self.assertEqual(result, prior_val)

    def testBLT(self):
        op = BLT("$t0", "$t1", "c")
        op.execute(self.branch_state)
        result = self.branch_state.program_counter()
        self.assertEqual(result, 2)

    def testBGE(self):
        prior_val = self.branch_state.program_counter()
        op = BGE("$t0", "$t1", "b")
        op.execute(self.branch_state)
        result = self.branch_state.program_counter()
        self.assertEqual(result, prior_val)

    def testBLE(self):
        op = BLE("$t0", "$t1", "b")
        op.execute(self.branch_state)
        result = self.branch_state.program_counter()
        self.assertEqual(result, 1)

    def testBGTU(self):
        prior_val = self.branch_state.program_counter()
        op = BGTU("$t0", "$t1", "b")
        op.execute(self.branch_state)
        result = self.branch_state.program_counter()
        self.assertEqual(result, prior_val)

    def testBGTZ(self):
        op = BGTZ("$t0", "c")
        op.execute(self.branch_state)
        result = self.branch_state.program_counter()
        self.assertEqual(result, 2)

if __name__ == "__main__":
    unittest.main()
