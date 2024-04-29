# pick item from a dropdown
not tag: user.homophones_open
-
choose <number_small>:      key("down:{number_small-1} enter")
choose up <number_small>:   key("up:{number_small} enter")

# DEPRECATED
drop down <number_small>:   app.notify("DEPRECATED: please use the voice command 'choose' instead of 'drop down'")
drop down up <number_small>: app.notify("DEPRECATED: please use the voice command 'choose up' instead of 'drop down up'")
