from __future__ import with_statement
import parser
from mipper import Program

def test1():
    fib_text = ""
    with open("fib.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            fib_text += line

    fib_prog = Program(fib_text)
    def report_memory(state):
        print state.currentInstruction()

    fib_prog.on_suspension = report_memory
    fib_prog.execute()

def test2():
    mem_text = ""
    with open("test1.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            mem_text += line

    mem_prog = Program(mem_text)
    mem_prog.execute()
    print str(mem_prog.state.memory),

def test3():
    io_text = ""
    with open("test2.asm") as f:
        for line in f:
            line = line.replace("\\n", "\n")
            io_text += line

    io_prog = Program(io_text)
    io_prog.execute()
    print str(io_prog.state.memory),

def perform_test():
    test1()
    test2()
    test3()


if __name__ == '__main__':
    perform_test()

