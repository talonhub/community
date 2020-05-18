code.language: go
-
variadic: "..."
logical and: " && "
logical or: " || "
# Many of these add extra terrible spacing under the assumption that
# gofmt/goimports will erase it.
state comment: "// "
[line] comment <phrase>:
    key("cmd-right")
    insert(" // ")
    insert(user.formatted_text(phrase, "sentence"))

# "add comment <phrase> [over]:
#     key("cmd-right")
#     text_with_leading(" // ")
# ]
# "[state] context: insert("ctx")
state (funk | func | fun): "func "
function (Annette | init) [over]: "func init() {\n"
function <phrase> [over]:
    insert("func ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))
    insert("(")
    sleep(100ms)

method <phrase> [over]:
    insert("meth ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))
    sleep(100ms)

state var: "var "
variable [<phrase>] [over]:
    insert("var ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))
    # insert(" ")
    sleep(100ms)

of type [<phrase>] [over]:
    insert(" ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

# "set <phrase> [over]:
#     insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))
#     insert(" := ")
#     sleep(100ms)
# ]
state break: "break"
state (chan | channel): " chan "
state go: "go "
state if: "if "
if <phrase> [over]:
  insert("if ")
  insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))
spawn <phrase> [over]:
  insert("go ")
  insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))
state else if: " else if "
else if <phrase> [over]:
    insert(" else if ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

state else: " else "
else <phrase> [over]:
    insert(" else {")
    key("enter")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

state while: "while "
while <phrase> [over]:
    insert("while ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

state for: "for "
for <phrase> [over]:
    insert("for ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

state for range: "forr "
range <phrase> [over]:
    insert("forr ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

state format: "fmt"
format <phrase> [over]:
    insert("fmt.")
    insert(user.formatted_text(phrase, "PUBLIC_CAMEL_CASE"))

state switch: "switch "
switch <phrase> [over]:
    insert("switch ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

state select: "select "
# "select <phrase>:insert("select "), insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE")]
state (const | constant): " const "
constant <phrase> [over]:
    insert("const ")
    insert(user.formatted_text(phrase, "PUBLIC_CAMEL_CASE"))

state case: " case "
state default: " default:"
case <phrase> [over]:
    insert("case ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

state type: " type "
type <phrase> [over]:
    insert("type ")
    insert(user.formatted_text(phrase, "PUBLIC_CAMEL_CASE"))
state true: " true "
state false: " false "
state (start | struct | struck):
  insert(" struct {")
  key("enter")
(struct | struck) <phrase> [over]:
    insert(" struct {")
    key("enter")
    insert(user.formatted_text(phrase, "PUBLIC_CAMEL_CASE"))

[state] empty interface: " interface{} "
state interface:
  insert(" interface {")
  key("enter")
interface <phrase> [over]:
    insert(" interface {")
    key("enter")
    insert(user.formatted_text(phrase, "PUBLIC_CAMEL_CASE"))

state string: " string "
[state] (int | integer | ant): "int"
state slice: " []"
slice of: "[]"
[state] (no | nil): "nil"
state (int | integer | ant) 64: " int64 "
state tag:
  insert(" ``")
  key("left")
field tag <phrase> [over]:
    insert(" ``")
    key("left")
    sleep(100ms)
    insert(user.formatted_text(phrase, "snake"))
    insert(" ")
    sleep(100ms)

state return: " return "
return  <phrase> [over]:
    insert("return ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

map of string to string: " map[string]string "
map of <phrase> [over]:
    insert("map[")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))
    key("right")
    sleep(100ms)

receive: " <- "
make: "make("
loggers [<phrase>] [over]:
    insert("logrus.")
    insert(user.formatted_text(phrase, "PUBLIC_CAMEL_CASE"))

length <phrase> [over]:
    insert("len(")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

append <phrase> [over]:
    insert("append(")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

state (air | err): "err"
error: " err "
loop over [<phrase>] [over]:
    insert("forr ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

item <phrase> [over]:
  insert(", ")
  insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

value <phrase> [over]:
    insert(": ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

address of [<phrase>] [over]:
    insert("&")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

pointer to [<phrase>] [over]:
    insert("*")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))

swipe [<phrase>] [over]:
    key("right")
    insert(", ")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))
