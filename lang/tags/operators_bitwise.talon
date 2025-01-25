tag: user.code_operators_bitwise
-

#bitwise operators
bitwise and:
    user.deprecate_command("2025-01-19", "bitwise and", "op bitwise and")
    user.code_operator("BITWISE_AND")

bitwise or:
    user.deprecate_command("2025-01-19", "bitwise or", "op bitwise or")
    user.code_operator("BITWISE_OR")

bitwise not:
    user.deprecate_command("2025-01-19", "bitwise not", "op bitwise not")
    user.code_operator("BITWISE_NOT")

(op | logical | bitwise) (ex | exclusive) or:
    user.deprecate_command("2025-01-19", "(op | logical | bitwise) (ex | exclusive) or", "op bitwise ex or")
    user.code_operator("BITWISE_EXCLUSIVE_OR")

(op | logical | bitwise) (left shift | shift left):
    user.deprecate_command("2025-01-19", "(op | logical | bitwise) (left shift | shift left)", "op bitwise left shift")
    user.code_operator("BITWISE_LEFT_SHIFT")

(op | logical | bitwise) (right shift | shift right):
    user.deprecate_command("2025-01-19", "(op | logical | bitwise) (right shift | shift right)", "op bitwise right shift")
    user.code_operator("BITWISE_RIGHT_SHIFT")
