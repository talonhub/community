mode: user.talon
mode: command 
and code.language: talon
-
tag(): user.code_operators
tag(): user.code_comment
action(user.code_operator_and): " and "
action(user.code_operator_or): " or "
action(user.code_operator_subtraction): " - "
action(user.code_operator_addition): " + "
action(user.code_operator_multiplication): " * "
action(user.code_operator_division): " / "
action(user.code_operator_assignment): " = "
action(user.code_comment): "#"

insert: 
	insert("insert('')")
	edit.left()
	edit.left()
key:
	insert('key()')
	edit.left()
control key:
	insert('ctrl')
super key:
	insert('super')
command key:
	insert('cmd')
alt key:
	insert('alt')
shift key:
	insert('shift')

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
settings:
	insert("settings():\n")
tag set:
	insert("tag(): ")
tag require:
	insert("tag: ")
user:
	insert("user.")

