register save {user.letter}:
    modified = "\"" + letter
    insert(modified + "y")

register {user.letter}:
    key(esc)
    modified = "\"" + letter
    insert(modified + "pa")
