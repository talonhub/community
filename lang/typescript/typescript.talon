mode: user.typescript
mode: command
and code.language: typescript
-
tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_generic

settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_variable_formatter = "PRIVATE_CAMEL_CASE"
    
(op | is) strict equal: " === "
(op | is) strict not equal: " !== "

state const: "const "

state let: "let "

state var: "var "

state async: "async "

state await: "await "

state map:
    insert(".map()")
    key(left)
    
state filter:
    insert(".filter()")
    key(left)
    
state reduce:
    insert(".reduce()")
    key(left)
    
state spread: "..."

^funky <user.text>$: user.code_default_function(text)
^pro funky <user.text>$: user.code_protected_function(text)
^pub funky <user.text>$: user.code_public_function(text)
