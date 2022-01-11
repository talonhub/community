tag: user.code_operators_assignment
-
tag(): user.code_operators_math
tag(): user.code_operators_bitwise

# assignment
op (equals | assign): user.code_operator_assignment()

# combined computation and assignment
op (minus | subtract) equals: user.code_operator_subtraction_assignment()
op (plus | add) equals: user.code_operator_addition_assignment()
op (times | multiply) equals: user.code_operator_multiplication_assignment()
op divide equals: user.code_operator_division_assignment()
op mod equals: user.code_operator_modulo_assignment()
[op] increment: user.code_operator_increment()

#bitwise operators
(op | logical | bitwise) (ex | exclusive) or equals: user.code_operator_bitwise_exclusive_or_equals()
[(op | logical | bitwise)] (left shift | shift left) equals: user.code_operator_bitwise_left_shift_equals()
[(op | logical | bitwise)] (left right | shift right) equals: user.code_operator_bitwise_right_shift_equals()
