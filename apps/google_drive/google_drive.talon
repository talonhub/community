app: google_drive
-

tag(): user.file_manager
tag(): user.navigation

# View and panel navigation
go nav: key("g n")
go files: key("g l")
view (grid | list): key("v")
show details: key("d")
show activity: key("i")
search drive: key("/")

# Item manipulation
file rename: key("n")
file share: key(".")
file move: key("z")
file star: key("s")
file preview: key("p")
(trash | remove) it: key("#")
clear selection: key("shift-n")

# File creation & uploads
new doc: key("shift-t")
new sheet | new spreadsheet: key("shift-s")
new slides | new presentation: key("shift-p")
new form: key("shift-o")
upload file: key("shift-u")
upload folder: key("shift-i")
create menu: key("c")
