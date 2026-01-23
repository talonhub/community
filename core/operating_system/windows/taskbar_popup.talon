tag: user.taskbar_canvas_popup_showing
-
go <number>: 
    print("taskbar")
    user.taskbar_popup(0, number - 1, 1)

go <number> connie: 
    user.taskbar_popup(1, number - 1, 1)

go <number> duke: 
    user.taskbar_popup(0, number - 1, 2)