code.language: cpp
-

tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_math
tag(): user.code_operators_pointer

# By default, user.cpp_standard_prefix is saying either "stood" or "standard"
{user.cpp_standard_prefix} {user.cpp_standard_type}: insert("std::{cpp_standard_type}")

#The default tag for this is for function support, so this is explicitly defined here until full function support is provided
type <user.code_type>: insert(code_type)
