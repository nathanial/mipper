from __future__ import with_statement
import parser
from mipper import Program
import logging



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='w')


def test1():
    fib_text = ""
    with open("fib.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            fib_text += line

    fib_prog = Program(fib_text)
    fib_prog.execute()

def test2():
    mem_text
    with open("test1.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            mem_text += line

    mem_prog = Program(mem_text)
    mem_prog.execute()

def perform_test():
    test1()

if __name__ == '__main__':
    perform_test()

