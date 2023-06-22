tag: user.talon
-
tag(): user.code_operators_math
tag(): user.code_operators_assignment
tag(): user.code_comment_line
tag(): user.code_functions_common
# uncomment user.talon_populate_lists tag to activate talon-specific lists of actions, scopes, modes etcetera.
# Do not enable this tag with dragon, as it will be unusable.
# with conformer, the latency increase may also be unacceptable depending on your cpu
# see https://github.com/knausj85/knausj_talon/issues/600
# tag(): user.talon_populate_lists

dot talon: insert(".talon")
#defintion blocks for the context
action block: user.insert_between("action(", "):")
setting block: insert("settings():\n\t")
setting {user.talon_settings}: user.paste("{talon_settings} = ")
#context requirements
win require: insert("os: windows\n")
mac require: insert("os: mac\n")
linux require: insert("os: linux\n")
title require: insert("win.title: ")
application [require] [{user.talon_apps}]:
    app = talon_apps or ""
    user.paste("app: {app}")
mode require [{user.talon_modes}]:
    mode = talon_modes or ""
    user.paste("mode: {mode}")
tag require [{user.talon_tags}]:
    tag = talon_tags or ""
    user.paste("tag: {tag}")
tag set [{user.talon_tags}]:
    tag = talon_tags or ""
    user.paste("tag(): {tag}")
host require:
    hostname = user.talon_get_hostname()
    user.paste("hostname: {hostname}\n")
# requires user.talon_populate_lists tag. do not use with dragon
list {user.talon_lists}: "{{{talon_lists}}}"
# requires user.talon_populate_lists tag. do not use with dragon
capture {user.talon_captures}: "<{talon_captures}>"

#commands for dictating key combos
key <user.keys> over: "{keys}"
key <user.modifiers> over: "{modifiers}"

# all actions (requires uncommenting user.talon_populate_lists tag above)
funk {user.talon_actions}:
    user.code_insert_function(talon_actions, edit.selected_text())
funk cell <number>: user.code_select_function(number - 1, "")
funk wrap <user.code_common_function>:
    user.code_insert_function(code_common_function, edit.selected_text())
funk wrap <number>: user.code_select_function(number - 1, edit.selected_text())
