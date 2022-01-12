mode: user.scala
mode: user.auto_lang
and code.language: scala
-
tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_block_comment
tag(): user.code_generic

settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_variable_formatter = "PRIVATE_CAMEL_CASE"

state package: "package "

state val: "val "
state var: "var "

state match: user.code_state_switch()

state case class: "case class "
state object: "object "

string: key('"')
char: key("'")
block string:
  insert('""""""')
  key("left left left")

# Methods
^funky <user.text>$: user.code_default_function(text)
^pro funky <user.text>$: user.code_protected_function(text)
^pri funky <user.text>$: user.code_private_function(text)
