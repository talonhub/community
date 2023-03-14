os: windows
and app.name: Windows Explorer
os: windows
and app.exe: Explorer.EXE

os:windows   
and title: /Save As/


-

address bar: 
    #select address bar
    key(alt-D) 
(hunt|search) bar: 
    #select search bar
    key(ctrl-e)
    #key(ctrl-f) 

window new:
    #open selected path in a new window
    key(ctrl-n)

window close:
    # close selected window
    key(ctrl-w)

bigger icons: 
    #make icons bigger
    key(ctrl:down)
    user.mouse_scroll_up(0.2)
    key(ctrl:up)

smaller icons: 
    #make icons smaller
    key(ctrl:down)
    user.mouse_scroll_down(0.2)
    key(ctrl:up)

parent folders: 
    #display all folders above the selected folder
    key(ctrl-shift-e)
    
    
create new folder: 
    #create new folder 
    key(ctrl-shift-n)

display subfolders: 
    # Display all subfolders under the selected folder.
    key(keypad_multiply)

expand folder:
    #display contents of selected folder
    key(keypad_plus)

collapse folder:
    #Collapse the selected folder.
    key(keypad_minus)

preview panel:
    #toggle display preview panel
    key(alt-p)

properties: 
    #display properties dialog for selected item
    key(alt-enter)

go forward:
    #view the next folder
    key(alt-right)

go back:
    #view the previous folder you were looking at
    key(alt-left)
    #key(backspace)

view parent [folder]:
    key(alt-up)

display selection:
    Display the current selection (if it's collapsed), or select the first subfolder.
    key(right)
    
collapse selection:
    #Collapse the current selection (if it's expanded), or select the folder that the folder was in.
    key(left)

bottom: 
    key(end)

top: 
    key(home)

rename:
    key(shift-f10)
    sleep(300ms)
    key(m)

left panel: key(f6:6)
right panel: key(f6)