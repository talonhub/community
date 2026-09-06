tag: user.code_operators_math
-

# math operators
op subtract:
    user.deprecate_command("2025-01-19", "op subtract", "op minus")
    user.code_operator("MATH_SUBTRACT")

op add:
    user.deprecate_command("2025-01-19", "op add", "op plus")
    user.code_operator("MATH_ADD")

op multiply:
    user.deprecate_command("2025-01-19", "op multiply", "op times")
    user.code_operator("MATH_MULTIPLY")

op (exponent | to the power [of]):
    user.deprecate_command("2025-01-19", "op (exponent | to the power [of])", "op power")
    user.code_operator("MATH_EXPONENT")

# comparison operators
is more:
    user.deprecate_command("2025-01-19", "is more", "is greater")
    user.code_operator("MATH_GREATER_THAN")

is below [than]:
    user.deprecate_command("2025-01-19", "is below [than]", "is less")
    user.code_operator("MATH_LESS_THAN")

is greater than or equal:
    user.deprecate_command("2025-01-19", "is greater than or equal", "is greater or equal")
    user.code_operator("MATH_GREATER_THAN_OR_EQUAL")

is less than or equal:
    user.deprecate_command("2025-01-19", "is less than or equal", "is less or equal")
    user.code_operator("MATH_LESS_THAN_OR_EQUAL")

# logical operators
logical and:
    user.deprecate_command("2025-01-19", "logical and", "op and")
    user.code_operator("MATH_AND")

logical or:
    user.deprecate_command("2025-01-19", "logical or", "op or")
    user.code_operator("MATH_OR")

logical not:
    user.deprecate_command("2025-01-19", "logical not", "op not")
    user.code_operator("MATH_NOT")

op colon:
    user.deprecate_command("2025-01-19", "op colon", "pad colon")
    insert(" : ")
