talon copy context: user.talon_add_context_clipboard()
<<<<<<< HEAD
talon copy title: 
    title = win.title()
    clip.set_text(title)
talon dump context: 
=======
talon dump context:
>>>>>>> master
    name = app.name()
    executable =  app.executable()
    bundle = app.bundle()
    title = win.title()
    print("Name: {name}")
    print("Executable: {executable}")
    print("Bundle: {bundle}")
    print("Title: {title}")

voice command show log: key(f20)