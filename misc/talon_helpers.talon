talon copy context: user.talon_add_context_clipboard()
talon dump context:
    name = app.name()
    executable =  app.executable()
    bundle = app.bundle()
    title = win.title()
    print("Name: {name}")
    print("Executable: {executable}")
    print("Bundle: {bundle}")
    print("Title: {title}")

voice command show log: key(f20)