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
m d five: "md5"
(regex | rejex): "regex"
const: "const "
static: "static "
tip pent: "int "
tip char: "char "
tip byte: "byte "
tip pent sixty four: "int64_t "
tip you went sixty four: "uint64_t "
tip pent thirty two: "int32_t "
tip you went thirty two: "uint32_t "
tip pent sixteen: "int16_t "
tip you went sixteen: "uint16_t "
tip pent eight: "int8_t "
tip you went eight: "uint8_t "
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
word Point two d: "Point2d"
word Point three d: "Point3d"
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
string U T F eight: 
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
volume up: key(volup)
volume down: key(voldown)
mute: key(mute)
play next: key(next)
play previous: key(prev)
(play | pause): key(play_pause)  
wipe: key(backspace)
(pad | padding): 
	insert("  ") 
	key(left)
funny: "ha ha"
#menu: key(alt)
