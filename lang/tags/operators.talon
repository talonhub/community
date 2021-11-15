tag: user.code_operators
-
#pointer operators
op dereference: user.code_operator_indirection()
op address of: user.code_operator_address_of()
op arrow: user.code_operator_structure_dereference()

#lambda
op lambda: user.code_operator_lambda()

#subscript
op subscript: user.code_operator_subscript()

#math operators
op (minus | subtract): user.code_operator_subtraction()
op (plus | add): user.code_operator_addition()
op (times | multiply): user.code_operator_multiplication()
op divide: user.code_operator_division()
op mod: user.code_operator_modulo()
(op (power | exponent) | to the power [of]): user.code_operator_exponent()

#comparison operators
(op | is) equal: user.code_operator_equal()
(op | is) not equal: user.code_operator_not_equal()
(op | is) (greater | more): user.code_operator_greater_than()
(op | is) (less | below) [than]: user.code_operator_less_than()
(op | is) greater [than] or equal: user.code_operator_greater_than_or_equal_to()
(op | is) less [than] or equal: user.code_operator_less_than_or_equal_to()
(op | is) in: user.code_operator_in()

#logical operators
(op | logical) and: user.code_operator_and()
(op | logical) or: user.code_operator_or()

#bitwise operators
[op] bitwise and: user.code_operator_bitwise_and()
[op] bitwise or: user.code_operator_bitwise_or()

# TODO: split these out into separate logical and bitwise operator commands
(op | logical | bitwise) (ex | exclusive) or: user.code_operator_bitwise_exclusive_or()
(op | logical | bitwise) (left shift | shift left): user.code_operator_bitwise_left_shift()
(op | logical | bitwise) (right shift | shift right): user.code_operator_bitwise_right_shift()

#tbd
(op | pad) colon: " : "
