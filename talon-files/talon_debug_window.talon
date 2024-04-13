# this functionality is only available in the talon beta
# note: these commands are only useful when the search box is focused
app: talon_debug_window
-
# uncomment user.talon_populate_lists tag to activate talon-specific lists of actions, scopes, modes etcetera.
# Do not enable this tag with dragon, as it will be unusable.
# with conformer, the latency increase may also be unacceptable depending on your cpu
# see https://github.com/talonhub/community/issues/600
# tag(): user.talon_populate_lists

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
