# specific comma entries
trash:
    ','
    key(enter)

llama:
    edit.line_end()
    key(left)
    ','
    key(enter)

# menu navigation
drop <number>:
    key("down:{number}")
    key(enter)

# easier your navigation
access:
    user.password_fill()
    sleep(500ms)
    key(enter)