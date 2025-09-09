code.language: cpp
-

tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_math
tag(): user.code_operators_pointer
tag(): user.code_functions_common

# e.g. "stood vector"
# To allow more easily dealing with generic types, a future update might include the number of generic type arguments in the string returned by the cpp_standard_type capture
<user.cpp_standard_type>: insert(cpp_standard_type)
<user.cpp_standard_constant>: insert(cpp_standard_constant)

[funk] <user.cpp_standard_function>: user.code_insert_function(cpp_standard_function, "")
funk wrap <user.cpp_standard_function>: user.code_insert_function(cpp_standard_function, edit.selected_text())

#The default tag for this is for function support, so this is explicitly defined here until full function support is provided
type <user.code_type>: insert(code_type)

# usage: type name followed by variable name
# example: "var stood string reference full name" -> "std::string &full_name"
var <user.variable_declaration>: insert(variable_declaration)

# We reserve use of the "import" command from the user.code_libraries tag for use with C++ modules.
include {user.cpp_standard_header}:
    user.insert_snippet_by_name_with_phrase("includeSystemStatement", user.cpp_standard_header)
    key(enter)
include system: user.insert_snippet_by_name("includeSystemStatement")
include local: user.insert_snippet_by_name("includeLocalStatement")
