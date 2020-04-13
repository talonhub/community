code.language: talon
-
action(user.language_operator_and): " and "
action(user.language_operator_or): " or "
action(user.language_operator_minus): " - "
action(user.language_operator_plus): " + "
action(user.language_operator_multiply): " * "
action(user.language_operator_divide): " / "
action(user.language_operator_assign): " = "
action(user.language_comment): "#"

insert: 
	insert('insert("")')
	edit.left()
	edit.left()
	
key:
	insert('key()')
	edit.left()

action:
	insert("action()")
	edit.left()

os win:
	insert("os: windows")
	
os mac:
	insert("os: mac")
	
os lunix:
	insert("os: linux")
	
app:
	insert("app: ")
	
tags:
	insert("tags: ")

user:
	s is ainsert("user.")

