from __future__ import with_statement
import parser
from mipper import Program, ProgramFactory
import unittest
from unittest import TestSuite, TestLoader, TestResult, TestCase

fib_list = [1,1,2,3,5,8,13,21,34,55,89]

def std_input():
    return raw_input("")
def std_output(val):
    print val,
def print_blah(state):
    print "BREAK"

program_factory = ProgramFactory(input = std_input,
                                 output = std_output,
                                 on_suspension = print_blah)

class IntegrationTests(TestCase):
    def testFib1(self):
        fib_text = ""
        with open("fib.asm") as f:
            for line in f:
                line = line.replace("\\n", "\n")
                fib_text += line

        output_list = []
        def mod_output(val):
            output_list.append(val)
        def mod_suspension(state):
            fib_prog.execute()

        fib_prog = program_factory.create_program(fib_text,
                                                  output = mod_output,
                                                  on_suspension = mod_suspension)
        fib_prog.execute()
        self.assertEqual(fib_list,
                         filter(lambda x: not type(x) is str, output_list[:-3]))

    def testFib2(self):
        mem_text = ""
        with open("test1.asm") as f:
            for line in f:
                line = line.replace("\\n", "\n")
                mem_text += line

        mem_prog = program_factory.create_program(mem_text)
        mem_prog.execute()
        self.assertEqual(fib_list, mem_prog.state.memory[:11])

    def test3(self):
        io_text = ""
        with open("test2.asm") as f:
            for line in f:
                line = line.replace("\\n", "\n")
                io_text += line

        def mod_input():
            return "blah"

        io_prog = program_factory.create_program(io_text, input = mod_input)
        io_prog.execute()
        self.assertEqual(['b','l','a','h'], io_prog.state.memory[:4])

    def test4(self):
        comp_text = ""
        with open("test4.asm") as f:
            for line in f:
                line = line.replace("\\n", "\n")
                comp_text += line

        comp_prog = program_factory.create_program(comp_text)
        comp_prog.execute()


if __name__ == '__main__':
    unittest.main()
