.data
theArray: .space 160

.text
main:
        li    $t6, 1              # Sets t6 to 1
        li    $t7, 4              # Sets t7 to 4
        sw    $t6, theArray($zero)   # Sets the first term to 1
        sw    $t6, theArray($t7)  # Sets the second term to 1
        li    $t0, 8              # Sets t0 to 8

loop:
        addi  $t3, $t0, -8
        addi  $t4, $t0, -4
        lw    $t1, theArray($t3)  # Gets the last
        lw    $t2, theArray($t4)  #   two elements
        add   $t5, $t1, $t2       # Adds them together...
        sw    $t5, theArray($t0)  # ...and stores the result
        addi  $t0, $t0, 4         # Moves to next "element" of theArray
        blt   $t0, 160, loop      # If not past the end of theArray, repeat
