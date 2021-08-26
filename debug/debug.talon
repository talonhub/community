talon debug running:
    user.switcher_toggle_running()
talon debug app:
    print("-------DEBUG APP-------")
    print(app.name())
    print(app.executable())
    print(win.title())
    print("-------DEBUG APP-------")
talon debug active context:
    user.debug_active_context()
^incorrect$: skip()
