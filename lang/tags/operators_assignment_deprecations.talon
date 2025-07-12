tag: user.code_operators_assignment
-
tag(): user.code_operators_math
tag(): user.code_operators_bitwise

# assignment
op assign:
    user.deprecate_command("2025-01-19", "op assign", "op equals")
    user.code_operator("ASSIGNMENT")

# combined computation and assignment
op subtract equals:
    user.deprecate_command("2025-01-19", "op subtract equals", "op minus equals")
    user.code_operator("ASSIGNMENT_SUBTRACTION")

op add equals:
    user.deprecate_command("2025-01-19", "op add equals", "op plus equals")
    user.code_operator("ASSIGNMENT_ADDITION")

op multiply equals:
    user.deprecate_command("2025-01-19", "op multiply equals", "op times equals")
    user.code_operator("ASSIGNMENT_MULTIPLICATION")

increment:
    user.deprecate_command("2025-01-19", "increment", "op increment")
    user.code_operator("ASSIGNMENT_INCREMENT")

#bitwise operators
[op] bit [wise] and equals:
    user.deprecate_command("2025-01-19", "[op] bit [wise] and equals", "op bitwise and equals")
    user.code_operator("ASSIGNMENT_BITWISE_AND")

[op] bit [wise] or equals:
    user.deprecate_command("2025-01-19", "[op] bit [wise] or equals", "op bitwise or equals")
    user.code_operator("ASSIGNMENT_BITWISE_OR")

(op | logical | bitwise) (ex | exclusive) or equals:
    user.deprecate_command("2025-01-19", "(op | logical | bitwise) (ex | exclusive) or equals", "op bitwise exclusive or equals")
    user.code_operator("ASSIGNMENT_BITWISE_EXCLUSIVE_OR")

[(op | logical | bitwise)] (left shift | shift left) equals:
    user.deprecate_command("2025-01-19", "[(op | logical | bitwise)] (left shift | shift left) equals", "op left shift equals")
    user.code_operator("ASSIGNMENT_BITWISE_LEFT_SHIFT")

[(op | logical | bitwise)] (right shift | shift right) equals:
    user.deprecate_command("2025-01-19", "[(op | logical | bitwise)] (right shift | shift right) equals", "op right shift equals")
    user.code_operator("ASSIGNMENT_BITWISE_RIGHT_SHIFT")
