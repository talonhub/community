win.title:/repl/
win.title:/Talon - REPL/
-
tag(): user.talon_python

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
^debug action {user.talon_actions}$:
    insert("actions.find('{user.talon_actions}')")
    key(enter)
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
