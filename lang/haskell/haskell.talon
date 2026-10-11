code.language: haskell
-

tag(): user.code_comment_line
tag(): user.code_comment_block
tag(): user.code_data_bool
tag(): user.code_data_null

# TODO: implement functions
tag(): user.code_functions

tag(): user.code_functions_common
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_lambda
tag(): user.code_operators_math


# TODO: complete tags 

# it is not assignement either!
op do equals: insert("<-")
op bind: insert("<-")