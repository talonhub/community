#Defines commands common to both python and talon files
tag: user.talon
tag: user.talon_python
-
tag set [{user.talon_tags}]:
    tag = talon_tags or ""
    user.paste("tag(): {tag}")
# requires user.talon_populate_lists tag. do not use with dragon
list {user.talon_lists}: "{{{talon_lists}}}"
# requires user.talon_populate_lists tag. do not use with dragon
capture {user.talon_captures}: "<{talon_captures}>"

setting block: insert("settings():\n\t")
setting {user.talon_settings}: user.paste("{talon_settings} = ")

#commands for dictating key combos
key <user.keys> over: "{keys}"
key <user.modifiers> over: "{modifiers}"



