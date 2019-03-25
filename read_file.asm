.data
arr: .word 1 2 3


arr2: .word 10 20 3

.text
addi x11 x0 3


add x12 x0 x11  #after instruction comment

#this is comment
    # another comment

addi x20 x0 -45

sub x5 x20 x12