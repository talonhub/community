mode: user.python
mode: command 
and code.language: python
-
logical and: " and "
logical or: " or "
state in: " in "
is not none: " is not None"
is none: "  None"
empty dict: "{}"
word (dickt | dictionary): "dict"
state (def | deaf | deft): "def "
state else if: "elif "
state if: "if "
state else: "else:"
state self: "self"
state while:
	insert("while ()")
	edit.left()
state for: "for "
state switch:
	insert("switch ()")
	edit.left()
state case:
	insert("case \nbreak;")
	edit.up()
state goto:
	insert("goto ")
state import:
	insert("import ")
state class: "class "
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
comment py: "# "
dunder in it: "__init__"
self taught: "self."
from import:
	insert("from import ")
	key(left)
	edit.word_left()
	key(space)
	edit.left()
for in:
	insert("for in ")
	key(left)
	edit.word_left()
	key(space)
	edit.left()
dock string:
    insert("\"\"\"")
    insert("\"\"\"")
    edit.left()
    edit.left()
    edit.left()
pie test: "pytest"
