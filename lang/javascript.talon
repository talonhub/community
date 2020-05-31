code.language: javascript
-

const:
  insert("const ")
let:
  insert("let ")
var:
  insert("var ")
async:
  insert("async ")
await:
  insert("await ")

action(user.code_if):
  insert("if ()")
  key(left)
  
action(user.code_else):
  insert(" else {")
  
action(user.code_else_if):
  insert(" else if ()")
  key(left)
  
action(user.code_switch):
  insert("switch ()")
  key(left)
  
action(user.code_case):
  insert("case :")
  
action(user.code_do_loop):
  insert("do {")
  key(enter)
  
action(user.code_while_loop):
  insert("while ()")
  key(left)")
  
action(user.code_for_loop):
  insert("for ()")
  key(left)
  
action(user.code_for_each_loop):
  insert(".forEach()")
  key(left)
  
action(user.code_to_integer):
  insert("parseInt()")
  key(left)
  
action(user.code_to_float):
  insert("parseFloat()")
  key(left)
  
action(user.code_to_string):
  insert("String()")
  key(left)

action(user.code_to_boolean):
  insert("Boolean()")
  key(left)
  
action(user.code_and):
  insert(" && ")
  
action(user.code_or):
  insert(" || ")
  
action(user.code_not):
  insert(" != ")
  
action(user.code_sysout):
  insert("console.log()")
  key(left)
  
action(user.code_import):
  insert("import ")

action(user.code_from):
  insert(" from \"")
  
action(user.code_block):
  insert(" {")
  key(enter)

action(user.code_function):
  insert("function ()")
  key(left:2)
  
action(user.code_lambda):
  insert("() => ")
  key(left:5)
  
action(user.code_class):
  insert("class ")
  
action(user.code_docstring):
  insert("/**  */")
  key(left:3)

action(user.code_comment):
  insert("// ")
    
action(user.code_long_comment):
  insert("/*  */")
  key(left:3)
  
action(user.code_return):
  insert("return ")
  
action(user.code_null):
  insert("null")
  
action(user.code_true):
  insert("true")
  
action(user.code_false):
  insert("false")

state reduce:
  insert(".reduce()")
  key(left)
  
state map:
  insert(".map()")
  key(left)
  
state filter:
  insert(".filter()")
  key(left)
  