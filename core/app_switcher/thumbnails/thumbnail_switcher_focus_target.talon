# "focus <app>" for apps on the launch list that aren't running: starts them. A running
# app's name means the same here as in thumbnail_switcher_all.talon's focus command
# (user.focus_targets carries the running list's values as-is), so running wins.
os: windows
tag: user.thumbnail_switcher_all
-
focus <user.focus_target>: user.switcher_focus(focus_target)
