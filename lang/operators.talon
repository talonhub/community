tag: user.code_operators
-
#pointer operators
<user.operator> dereference: user.code_operator_indirection()
<user.operator> address of: user.code_operator_address_of()
<user.operator> arrow: user.code_operator_structure_dereference()

#lambda
<user.operator> lambda: user.code_operator_lambda()

#subscript
<user.operator> subscript: user.code_operator_subscript()

#assignment
<user.operator> (equals | assign): user.code_operator_assignment()

#math operators
<user.operator> (minus | subtract): user.code_operator_subtraction()
<user.operator> (minus | subtract) equals: user.code_operator_subtraction_assignment()
<user.operator> (plus | add): user.code_operator_addition()
<user.operator> (plus | add) equals: user.code_operator_addition_assignment()
<user.operator> (times | multiply): user.code_operator_multiplication()
<user.operator> (times | multiply) equals: user.code_operator_multiplication_assignment()
<user.operator> divide: user.code_operator_division()
<user.operator> divide equals: user.code_operator_division_assignment()
<user.operator> mod: user.code_operator_modulo()
<user.operator> mod equals: user.code_operator_modulo_assignment()
(<user.operator> (power | exponent) | to the power [of]): user.code_operator_exponent()

#comparison operators
(<user.operator> | is) equal: user.code_operator_equal()
(<user.operator> | is) not equal: user.code_operator_not_equal()
(<user.operator> | is) (greater | more): user.code_operator_greater_than()
(<user.operator> | is) (less | below) [than]: user.code_operator_less_than()
(<user.operator> | is) greater [than] or equal: user.code_operator_greater_than_or_equal_to()
(<user.operator> | is) less [than] or equal: user.code_operator_less_than_or_equal_to()
(<user.operator> | is) in: user.code_operator_in()

#logical operators
(<user.operator> | logical) and: user.code_operator_and()
(<user.operator> | logical) or: user.code_operator_or()

#bitwise operators
[<user.operator>] bitwise and: user.code_operator_bitwise_and()
(<user.operator> | logical | bitwise) and equals: user.code_operator_bitwise_and_equals()
[<user.operator>] bitwise or: user.code_operator_bitwise_or()
(<user.operator> | logical | bitwise) or equals: user.code_operator_bitwise_or_equals()
(<user.operator> | logical | bitwise) (ex | exclusive) or: user.code_operator_bitwise_exclusive_or()
(<user.operator> | logical | bitwise) (left shift | shift left): user.code_operator_bitwise_left_shift()
(<user.operator> | logical | bitwise) (right shift | shift right): user.code_operator_bitwise_right_shift()
(<user.operator> | logical | bitwise) (ex | exclusive) or equals: user.code_operator_bitwise_exclusive_or_equals()
[(<user.operator> | logical | bitwise)] (left shift | shift left) equals: user.code_operator_bitwise_left_shift_equals()
[(<user.operator> | logical | bitwise)] (left right | shift right) equals: user.code_operator_bitwise_right_shift_equals()

#tbd