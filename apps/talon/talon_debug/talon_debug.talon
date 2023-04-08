app: talon_debug
-
tag {user.talon_tags}:
    user.paste("{talon_tags}")

#commands for dictating key combos
key <user.keys> over: "{keys}"
key <user.modifiers> over: "{modifiers}"

action {user.talon_actions}:
    insert(talon_actions)
# requires user.talon_populate_lists tag. do not use with dragon
list {user.talon_lists}: "{talon_lists}"

# requires user.talon_populate_lists tag. do not use with dragon
capture {user.talon_captures}: "{talon_captures}"
set {user.talon_settings}: user.paste("{talon_settings}")
host:
    hostname = user.talon_get_hostname()
    user.paste("{hostname}")
application {user.talon_apps}:
    user.paste("{talon_apps}")
mode {user.talon_modes}:
    user.paste("{talon_modes}")