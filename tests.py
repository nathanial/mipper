import parser
from mipper import State
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='w')

fib_prog = """
.text

main:
li $t0, 0
li $t1, 1
li $t3, 0
li $t4, 10
li $t5, 0
li $t6, 1
li $t7, 2

jal Loop

print_space:
li $v0, 4
la $a0, space
syscall
jr $ra

print_b:
li $v0, 1
move $a0, $t1
syscall
jr $ra

print_odd_sum:
li $v0, 4
la $a0, odd_str
syscall
li $v0, 1
move $a0, $t6
syscall
jr $ra

print_even_sum:
li $v0, 4
la $a0, even_str
syscall
li $v0, 1
move $a0, $t5
syscall
jr $ra

Loop:
jal print_b
jal print_space

move $t2, $t0
move $t0, $t1
add $t1, $t0, $t2
addi $t3, $t3, 1

div $t1, $t7
mfhi $t8
beq $t8, $zero, even
j odd

even:
add $t5, $t5, $t1
blt $t3, $t4, Loop
j end

odd:
add $t6, $t6, $t1
blt $t3, $t4, Loop
j end

end:
jal print_b
jal print_even_sum
jal print_odd_sum

.data
space: .asciiz " "
odd_str: .asciiz "\nOdd Sum = "
even_str: .asciiz "\nEven Sum = "
"""

test_prog = """
.text
li $t0, 0
li $t1, 10
LOOP:
addi $t0, $t0, 1
bne $t0, $t1, LOOP
la $a0, space
.data
space: " "
"""

def perform_test():
    fib_prog2 = "".join(filter(lambda x: x.strip() != "", fib_prog.splitlines(True)))
    allocations, instructions = parser.parse("program",fib_prog2)
    state = State(instructions, allocations)
    while state.has_next():
        state.next()

    logging.debug(instructions)
    logging.debug(allocations)

if __name__ == '__main__':
    perform_test()

