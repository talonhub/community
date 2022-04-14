win.title:/repl/
win.title:/Talon - REPL/
-
tag(): user.talon_python

# uncomment user.talon_populate_lists tag to activate talon-specific lists of actions, scopes, modes etcetera.
# Do not enable this tag with dragon, as it will be unusable.
# with conformer, the latency increase may also be unacceptable depending on your cpu
# see https://github.com/knausj85/knausj_talon/issues/600
# tag(): user.talon_populate_lists

^test last$:
    phrase = user.history_get(1)
    command = "sim('{phrase}')"
    insert(command)
    key(enter)
^test <phrase>$:
    insert("sim('{phrase}')")
    key(enter)
^test numb <number_small>$:
    phrase = user.history_get(number_small)
    command = "sim('{phrase}')"
    #to do: shouldn't this work?
    #user.paste("sim({phrase})")
    insert(command)
    key(enter)
# requires user.talon_populate_lists tag. do not use with dragon
^debug action {user.talon_actions}$:
    insert("actions.find('{user.talon_actions}')")
    key(enter)
# requires user.talon_populate_lists tag. do not use with dragon
^debug list {user.talon_lists}$:
    insert("actions.user.talon_pretty_print(registry.lists['{talon_lists}'])")
    key(enter)
^debug tags$:
    insert("actions.user.talon_pretty_print(registry.tags)")
    key(enter)
^debug settings$:
    insert("actions.user.talon_pretty_print(registry.settings)")
    key(enter)
^debug modes$:
    insert("actions.user.talon_pretty_print(scope.get('mode'))")
    key(enter)
# requires user.talon_populate_lists tag. do not use with dragon
^debug scope {user.talon_scopes}$:
    insert("actions.user.talon_pretty_print(scope.get('{talon_scopes}'))")
    key(enter)
^debug running apps$:
    insert("actions.user.talon_pretty_print(ui.apps(background=False))")
    key(enter)
^debug all windows$:
    insert("actions.user.talon_pretty_print(ui.windows())")
    key(enter)
^debug {user.running} windows$:
    insert("actions.user.talon_debug_app_windows('{running}')")
    key(enter)
