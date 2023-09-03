tag: user.code_object_oriented
-

{user.code_self} dot:
    insert(code_self)
    user.code_operator_object_accessor()

state {user.code_self}: insert(code_self)

state class: user.code_define_class()

{user.code_self} {user.code_operator_object_accessor}:
    insert("{code_self}{code_operator_object_accessor}")
