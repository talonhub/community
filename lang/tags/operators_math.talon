tag: user.code_operators_math
-

# math operators
op (minus | subtract): user.code_operator_subtraction()
op (plus | add): user.code_operator_addition()
op (times | multiply): user.code_operator_multiplication()
op divide: user.code_operator_division()
op mod: user.code_operator_modulo()
(op (power | exponent) | to the power [of]): user.code_operator_exponent()

# comparison operators
(op | is) equal: user.code_operator_equal()
(op | is) not equal: user.code_operator_not_equal()
(op | is) (greater | more): user.code_operator_greater_than()
(op | is) (less | below) [than]: user.code_operator_less_than()
(op | is) greater [than] or equal: user.code_operator_greater_than_or_equal_to()
(op | is) less [than] or equal: user.code_operator_less_than_or_equal_to()

# logical operators
(op | logical) and: user.code_operator_and()
(op | logical) or: user.code_operator_or()

# TODO: This operator should either be abstracted into a function or removed.
(op | pad) colon: " : "
