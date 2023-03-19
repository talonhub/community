tag: user.code_operators_assignment
-
tag(): user.code_operators_math
tag(): user.code_operators_bitwise

# assignment
do (equals | assign): user.code_operator_assignment()

# combined computation and assignment
do (minus | subtract) equals: user.code_operator_subtraction_assignment()
do (plus | add) equals: user.code_operator_addition_assignment()
do (times | multiply) equals: user.code_operator_multiplication_assignment()
do divide equals: user.code_operator_division_assignment()
do mod equals: user.code_operator_modulo_assignment()
[do] increment: user.code_operator_increment()

#bitwise operators
[do] bit [wise] and equals: user.code_operator_bitwise_and_assignment()
[do] bit [wise] or equals: user.code_operator_bitwise_or_assignment()
(do | logical | bitwise) (ex | exclusive) or equals:
    user.code_operator_bitwise_exclusive_or_assignment()
[(do | logical | bitwise)] (left shift | shift left) equals:
    user.code_operator_bitwise_left_shift_assignment()
[(do | logical | bitwise)] (right shift | shift right) equals:
    user.code_operator_bitwise_right_shift_assignment()
