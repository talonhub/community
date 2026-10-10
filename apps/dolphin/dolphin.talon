app: dolphin
-

tag(): user.address
tag(): user.tabs
tag(): user.file_manager
tag(): user.navigation

(refresh | reload) it: key("f5")
file rename: key("f2")

# Toggle right info panel. Named info internally, analagous to VScode/other apps' panels.
panel switch | info switch: key("f11")
# Toggle left nav bar
bar switch | places switch: key("f9")
folders switch: key("f7")
terminal switch: key("f4")
# Toggle breadcrumbs vs editable address
breadcrumb switch: key("f6")
