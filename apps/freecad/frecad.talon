app: freecad
-

look {user.freecad_view}: key(freecad_view)

create {user.freecad_geometry}: insert(freecad_geometry)

constrain {user.freecad_constraints}: insert(freecad_constraints)

varset | variable: insert("VarSet.")

toggle construction: insert("gn")

project: insert("gx")

export file: key("cmd-e")

save file: key("cmd-s")
