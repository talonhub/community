state if:
  user.code_if()
state else:
  user.code_else()
state else if:
  user.code_else_if()

states switch:
  user.code_switch()
state case:
  user.code_case()

loop do:
  user.code_do_loop()
loop while:
  user.code_while_loop()
loop for:
  user.code_for_loop()
loop each:
  user.code_for_each_loop()

to int:
  user.code_to_integer()
to float:
  user.code_to_float()
to string:
  user.code_to_string()
to bool:
  user.code_to_boolean()

logical and:
  user.code_and()
logical or:
  user.code_or()
logical not:
  user.code_not()

sys out:
  user.code_sysout()

state import:
  user.code_import()
state from:
  user.code_from()

state block:
  user.code_block()
state function:
  user.code_function()
state lambda:
  user.code_lambda()
state class:
  user.code_class()

docstring:
  user.code_docstring()
comment:
  user.code_comment()
long comment:
  user.code_long_comment()

state return:
  user.code_return()

value null:
  user.code_null()
value true:
  user.code_true()
value false:
  user.code_false()