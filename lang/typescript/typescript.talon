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

[state] const: "const "

[state] let: "let "

state var: "var "

state async: "async "
function: "function"

state await: "await "
undefined: "undefined"
return: "return "
[state] export: "export "
[state] new: "new "
state map:
    insert(".map()")
    key(left)
    
state filter:
    insert(".filter()")
    key(left)
state null: user.code_null()
state reduce:
    insert(".reduce()")
    key(left)
    
state if: user.code_state_if()
state spread: "..."

# Here actually we would like to use the snippet directly, but currently I don't know of a way to do that.
lion [<user.text>]:
    user.vscode("")
    sleep(50ms)
    insert(text or "")
    
debug:
    insert("clg")
    sleep(150ms)
    key(enter)
    
debug string [<user.text>]:
    insert("clg")
    sleep(150ms)
    key(enter)
    insert("\"")
    insert(text or "")
    key(end enter)
    
debug line:
    insert("console.log(\"=\".repeat(50));")
    
^funky <user.text>$: user.code_default_function(text)
^pro funky <user.text>$: user.code_protected_function(text)
^pub funky <user.text>$: user.code_public_function(text)
call:
    insert("()")
    key(left)
