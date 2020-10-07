talon copy context: user.talon_add_context_clipboard()
talon copy title: 
    title = win.title()
    clip.set_text(title)
talon dump context: 
    name = app.name()
    executable =  app.executable()
    bundle = app.bundle()
    title = win.title()
    print("Name: {name}")
    print("Executable: {executable}")
    print("Bundle: {bundle}")
    print("Title: {title}")
