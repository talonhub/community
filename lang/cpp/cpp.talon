code.language: cpp
-

tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_math
tag(): user.code_operators_pointer

# e.g. "stood vector"
# To allow more easily dealing with generic types, a future update might include the number of generic type arguments in the string returned by the cpp_standard_type capture
<user.cpp_standard_type>: insert(cpp_standard_type)

#The default tag for this is for function support, so this is explicitly defined here until full function support is provided
type <user.code_type>: insert(code_type)

see (none | null): "NULL"
is see (none | null): " == NULL"
is not see (none | null): " != NULL"