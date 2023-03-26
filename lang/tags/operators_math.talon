tag: user.code_operators_math
-

# math operators
do (minus | subtract): user.code_operator_subtraction()
do (plus | add): user.code_operator_addition()
do (times | multiply): user.code_operator_multiplication()
do divide: user.code_operator_division()
do mod: user.code_operator_modulo()
(do (power | exponent) | to the power [of]): user.code_operator_exponent()

# comparison operators
(do | is) equal: user.code_operator_equal()
(do | is) not equal: user.code_operator_not_equal()
(do | is) (greater | more): user.code_operator_greater_than()
(do | is) (less | below) [than]: user.code_operator_less_than()
(do | is) greater [than] or equal: user.code_operator_greater_than_or_equal_to()
(do | is) less [than] or equal: user.code_operator_less_than_or_equal_to()

# logical operators
(do | logical) and: user.code_operator_and()
(do | logical) or: user.code_operator_or()

# set operators
(do | is) in: user.code_operator_in()
(do | is) not in: user.code_operator_not_in()

# TODO: This operator should either be abstracted into a function or removed.
(do | pad) colon: " : "
