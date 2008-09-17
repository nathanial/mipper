from __future__ import with_statement
import mips_parser
from mipper import State
import logging



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='w')


def test1():
    fib_prog = ""
    with open("fib.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            fib_prog += line

    allocations, instructions = mips_parser.parse("program", fib_prog)
    state = State(instructions, allocations)
    while state.has_next():
        state.next()

def test2():
    mem_prog = ""
    with open("test1.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            mem_prog += line

    allocations, instructions = mips_parser.parse("program", mem_prog)
    state = State(instructions, allocations)
    while state.has_next():
        state.next()

def perform_test():
    test1()

if __name__ == '__main__':
    perform_test()

