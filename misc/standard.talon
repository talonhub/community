dragon words: "<dgnwords>"
dragon dictation: "<dgndictation>"
slap: key(home enter)
cd: "cd "
#cd talon home: "cd {}\n".format(TALON_HOME),
#cd talon user: "cd {}\n".format(TALON_USER),
#cd talon [user] emily: "cd {}/emily\n".format(TALON_USER),
#cd talon plugins: "cd {}\n".format(TALON_PLUGINS),
#talon logs: "cd {} && tail -f talon.log\n".format(TALON_HOME),
grep: "grep "
elle less: "ls "
run L S: "ls\n"
run (S S H | S H): "ssh"
(ssh | sh): "ssh "
ack: "ack "
diff: "diff "
dot pie: ".py"
run vim: "vim "
run make: "make\n"
run jobs: "jobs\n"
run make (durr | dear): "mkdir "
(jay son | jason ): "json"
(http | htp): "http"
tls: "tls"
md5: "md5"
(regex | rejex): "regex"
const: "const "
static: "static "
tip pent: "int "
tip char: "char "
tip byte: "byte "
tip pent 64: "int64_t "
tip you went 64: "uint64_t "
tip pent 32: "int32_t "
tip you went 32: "uint32_t "
tip pent 16: "int16_t "
tip you went 16: "uint16_t "
tip pent 8: "int8_t "
tip you went 8: "uint8_t "
tip size: "size_t"
tip float: "float "
tip double: "double "
args: 
	insert("()")
	key(left)
[inside] (index | array): 
	insert("[]") 
	key(left)
block: 
	insert("{}") 
	key(left enter enter up tab)
empty array: "[]"
comment see: "// "
word queue: "queue"
word eye: "eye"
word bson: "bson"
word iter: "iter"
word no: "NULL"
word cmd: "cmd"
word dup: "dup"
word streak: 
	insert("streq()") 
	key(left)
word printf: "printf"
word shell: "shell"
word Point2d: "Point2d"
word Point3d: "Point3d"
title Point: "Point"
word angle: "angle"
dunder in it: "__init__"
self taught: "self."
(dickt in it | inside bracket | in bracket): 
	insert("{}") 
	key(left)
(in | inside) percent: 
	insert("%%") 
	key(left)
list in it: 
	insert("[]") 
	key(left)
string utf8: 
	insert("'utf8'")
state past: "pass"

zoom [in]: edit.zoom_in()
zoom out: edit.zoom_out()
(page | scroll) up: key(pgup)
(page | scroll) [down]: key(pgdown)
copy: edit.copy()
cut: edit.cut()
paste: edit.paste()
#menu help: key(F1)
#spotlight: key(super)
(undo | under | skunks): edit.undo()
redo: edit.redo()
volume up: key(volume_up)
volume down: key(volume_down)
mute: key(mute)
play next: key(next)
play previous: key(previous)
(play | pause): key(space)  
wipe: key(backspace)
(pad | padding): 
	insert("  ") 
	key(left)
funny: "ha ha"
#menu: key(alt)
