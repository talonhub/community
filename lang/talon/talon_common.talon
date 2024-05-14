#Defines commands common to both python and talon files
code.language: talon
code.language: python
and tag: user.talon_python
-
tag set [{user.talon_tags}]:
    tag = talon_tags or ""
    user.talon_code_enable_tag(tag)

# requires user.talon_populate_lists tag. do not use with dragon
list {user.talon_lists}: "{{{talon_lists}}}"
# requires user.talon_populate_lists tag. do not use with dragon
capture {user.talon_captures}: "<{talon_captures}>"

setting {user.talon_settings}: user.talon_code_enable_setting(talon_settings)

#commands for dictating key combos
key <user.keys> over: "{keys}"
key <user.modifiers> over: "{modifiers}"

action {user.talon_actions}:
    user.talon_code_insert_action_call(talon_actions, edit.selected_text())
