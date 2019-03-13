.data
arr: .word 1 2 3


arr2: .word 10 20 3

.text
la x10 arr #start address
addi x11 x0 3 #arr_size
addi x12 x0 9 # s
addi x20 x0 0

BINARY_SEARCH:
beq x11 x0 not_found
srli x5 x11 1
slli x5 x5 2
add x18 x5 x10
lw x19 0(x18)
addi x20 x20 1
bge x20 x11 not_found
blt x12 x19 left
bge x12 x19 right
left:
srli x11 x11 1
jal x0 BINARY_SEARCH
right:
beq x19 x12 EXIT
addi x10 x18 0
srli x11 x11 1
addi x11 x11 1
jal x0 BINARY_SEARCH
        
EXIT:
add x10 x18 x0
jal x0 FALL_THRU
not_found:
addi x10 x0 -1

FALL_THRU: