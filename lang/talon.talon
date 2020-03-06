code.language: talon
-
action(user.knausj_talon.code.lang.comment_here):
    insert("#")

action(user.knausj_talon.code.lang.comment_begin_line):
    edit.line_start()
    insert("#")

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
	insert("user.knausj_talon.code.")

