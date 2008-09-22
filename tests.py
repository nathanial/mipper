from __future__ import with_statement
import parser
from mipper import Program, ProgramFactory
from unittest import TestSuite, TestLoader, TestResult
from Mipper.gnrl_tests import TestGeneralOperations
from Mipper.bool_tests import TestBoolOperations
from Mipper.math_tests import TestMathOperations
from Mipper.pseudo_tests import TestPseudoOperations

def std_input():
    return raw_input("")
def std_output(val):
    print val,
def print_blah(state):
    print "BREAK"

program_factory = ProgramFactory(input = std_input,
                                 output = std_output,
                                 on_suspension = print_blah)

def test1():
    fib_text = ""
    with open("fib.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            fib_text += line

    fib_prog = program_factory.create_program(fib_text)
    fib_prog.execute()
    fib_prog.execute()
    print ""

def test2():
    mem_text = ""
    with open("test1.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            mem_text += line

    mem_prog = program_factory.create_program(mem_text)
    mem_prog.execute()
    print str(mem_prog.state.memory),
    print ""

def test3():
    io_text = ""
    with open("test2.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            io_text += line

    io_prog = program_factory.create_program(io_text)
    io_prog.execute()
    print str(io_prog.state.memory),
    print ""

def run_suite(suite):
    result = TestResult()
    suite.run(result)
    return result

def perform_test():
    math_tests = TestLoader().loadTestsFromTestCase(TestMathOperations)
    bool_tests = TestLoader().loadTestsFromTestCase(TestBoolOperations)
    pseudo_tests = TestLoader().loadTestsFromTestCase(TestPseudoOperations)
    gnrl_tests = TestLoader().loadTestsFromTestCase(TestGeneralOperations)
    r1 = run_suite(math_tests)
    r2 = run_suite(bool_tests)
    r3 = run_suite(pseudo_tests)
    r4 = run_suite(gnrl_tests)
    print r1
    print r2
    print r3
    print r4
    if not (r1.wasSuccessful() and
            r2.wasSuccessful() and
            r3.wasSuccessful() and
            r4.wasSuccessful()):
        raise "Unit Tests Failed"

    test1()
    test2()
    test3()

if __name__ == '__main__':
    perform_test()

