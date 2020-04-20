code.language: talon
-
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
	insert("user.")
	
comment: 
	edit.line_start()
	insert("#")
