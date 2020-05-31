code.language: python
-

action(user.code_if):
  insert("if :")
  key(left)
  
action(user.code_else):
  insert("else:")
  
action(user.code_else_if):
  insert("elif :")
  key(left)
  
action(user.code_switch):
  insert("switch :")
  key(left)

action(user.code_case):
  insert("case \nbreak;")
  edit.up()
  
action(user.code_do_loop):
  insert("while True:")
  key(enter)
  
action(user.code_while_loop):
  insert("while :")
  key(left)
  
action(user.code_for_loop):
  insert("for :")
  key(left)
  
action(user.code_for_each_loop):
  user.code_for_loop()
  
action(user.code_to_integer):
  insert("int(")
  
action(user.code_to_float):
  insert("float(")
  
action(user.code_to_string):
  insert("str(")

action(user.code_to_boolean):
  insert("bool(")
  
action(user.code_and):
  insert(" and ")
  
action(user.code_or):
  insert(" or ")
  
action(user.code_not):
  insert(" != ")
  
action(user.code_sysout):
  insert("print(")
  
action(user.code_import):
  insert("import ")

action(user.code_from):
  insert("from ")
  
# action(user.code_block):

action(user.code_function):
  insert("def ():")
  key(left:2)
  
action(user.code_lambda):
  insert("lambda :")
  key(left)
  
action(user.code_class):
  insert("class :")
  
action(user.code_docstring):
  insert("\"\"\"\"\"\"")
  key(left:3)

action(user.code_comment):
  insert("# ")
  
action(user.code_long_comment):
  insert("\"\"\"\"\"\"")
  key(left:3)
  
action(user.code_return):
  insert("return ")
  
action(user.code_null):
  insert("None")
  
action(user.code_true):
  insert("True")
  
action(user.code_false):
  insert("False")

in:
  insert(" in ")

is:
  insert(" is ")

is not:
  insert(" is not ")

not:
  insert(" not ")

empty dict: "{}"

word (dickt | dictionary): "dict"

state include: "#include "

state include system:
  insert("#include <>")
  edit.left()

state include local:
  insert('#include ""')
  edit.left()

state type deaf: "typedef "

state type deaf struct:
  insert("typedef struct")
  insert("{{\n\n}}")
  edit.up()
  key(tab)

dunder in it: "__init__"

self taught: "self."

from import:
  insert("from  import ")
  key(left:8)

for in:
  insert("for  in ")
  key(left:4)

pie test: "pytest"
  