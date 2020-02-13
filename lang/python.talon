code.language: python
-
empty dict: insert("{}")
word (dickt | dictionary): "dict"
state (def | deaf | deft): "def "
state else if: "elif "
state if: "if "
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
state class: insert("class ")
state include: insert("#include ")
state include system: 
	insert("#include <>")
	edit.left()
state include local:
	insert('#include ""') 
	edit.left()
state type deaf: insert("typedef ")
state type deaf struct: 
	insert("typedef struct")
	insert("{{\n\n}}")
	edit.up()
	key(tab)
comment py: insert("# ")
dunder in it: insert("__init__")
self taught: 
	insert("self.")
from import: 
	insert("from import ")
	edit.word_left()
	key(space) 
	edit.left()
for in: 
	insert("for in ")
	edit.word_left()
	key(space) 
	edit.left()
	
