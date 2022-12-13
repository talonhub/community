tag: user.code_functions
-
^funky <user.text>$: user.code_default_function(text)
^pro funky <user.text>$: user.code_protected_function(text)
^pub funky <user.text>$: user.code_public_function(text)
^static funky <user.text>$: user.code_private_static_function(text)
^pro static funky <user.text>$: user.code_protected_static_function(text)
^pub static funky <user.text>$: user.code_public_static_function(text)

# for annotating function parameters
is type <user.code_type>: user.code_insert_type_annotation(code_type)
returns [type] <user.code_type>: user.code_insert_return_type(code_type)

# for generic reference of types
type <user.code_type>: insert(code_type)
