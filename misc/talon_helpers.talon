polo context copy pie: user.talon_add_context_clipboard_python()
polo context copy: user.talon_add_context_clipboard()
polo title copy: 
    title = win.title()
    clip.set_text(title)
polo dump context: 
    name = app.name()
    executable =  app.executable()
    bundle = app.bundle()
    title = win.title()
    print("Name: {name}")
    print("Executable: {executable}")
    print("Bundle: {bundle}")
    print("Title: {title}") 
