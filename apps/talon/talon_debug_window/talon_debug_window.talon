app: talon_debug_window
-
tag {user.talon_tags}: "{talon_tags}"

#commands for dictating key combos
key <user.keys> over: "{keys}"
key <user.modifiers> over: "{modifiers}"

action {user.talon_actions}: "{talon_actions}"
# requires user.talon_populate_lists tag. do not use with dragon
list {user.talon_lists}: "{talon_lists}"

# requires user.talon_populate_lists tag. do not use with dragon
capture {user.talon_captures}: "{talon_captures}"
set {user.talon_settings}: "{talon_settings}"
application {user.talon_apps}: "{talon_apps}"
