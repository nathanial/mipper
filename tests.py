from __future__ import with_statement
import parser
from mipper import ProgramFactory
import unittest
from Mipper.math_tests import TestMathOperations
from Mipper.bool_tests import TestBoolOperations
from Mipper.gnrl_tests import TestGeneralOperations
from Mipper.pseudo_tests import TestPseudoOperations

def program_out(x):
    print  x,

def program_in():
    return raw_input("")

def report_memory(state):
    print state.currentInstruction()


pf = ProgramFactory(input_function = program_in,
                    output_function = program_out,
                    on_suspension = report_memory)

def test1():
    fib_text = ""
    with open("fib.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            fib_text += line

    fib_prog = pf.create_program(fib_text)
    fib_prog.execute()
    fib_prog.execute()

def test2():
    mem_text = ""
    with open("test1.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            mem_text += line

    mem_prog = pf.create_program(mem_text)
    mem_prog.execute()
    print ""
    print str(mem_prog.state.memory)

def test3():
    io_text = ""
    with open("test2.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            io_text += line

    io_prog = pf.create_program(io_text)
    io_prog.execute()
    print ""
    print str(io_prog.state.memory)

def run_suite(suite):
    result = unittest.TestResult()
    suite.run(result)
    print result
    if not result.wasSuccessful():
        raise "Test Failed"

def perform_test():
    test1()
    test2()
    test3()
    math_tests = unittest.TestLoader().loadTestsFromTestCase(TestMathOperations)
    bool_tests = unittest.TestLoader().loadTestsFromTestCase(TestBoolOperations)
    gnrl_tests = unittest.TestLoader().loadTestsFromTestCase(TestGeneralOperations)
    pseudo_tests = unittest.TestLoader().loadTestsFromTestCase(TestPseudoOperations)

    print "Testing Math ",
    run_suite(math_tests)

    print "Testing Bool ",
    run_suite(bool_tests)

    print "Testing Gnrl ",
    run_suite(gnrl_tests)

    print "Testing Pseudo ",
    run_suite(pseudo_tests)

if __name__ == '__main__':
    perform_test()

