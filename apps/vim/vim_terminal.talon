win.title: /VIM MODE:t/
-
tag(): terminal

(pop terminal|vim mode):
    key(ctrl-\ ctrl-n)

rabbit up:
    key(ctrl-\ ctrl-n ctrl-b)

# this causes exclusive terminal windows to exit without requiring key press or
# dropping to a new empty buffer
exit terminal:
    key(ctrl-\)
    key(ctrl-n)
    insert("ZQ")

shadow <number_small>:
    user.vim_normal_mode_exterm("{number_small}k")
    key('0')
    insert("y$")
    insert(":set nohls\n")
    user.vim_set_insert_mode()
    edit.paste()
    key(space)

shadow last <number_small>:
    user.vim_normal_mode_exterm("{number_small}k")
    insert('$T ')
    insert("yW")
    user.vim_set_insert_mode()
    edit.paste()
    key(space)

# XXX - make this command copy the whole line like above, and have a different
# command that operates on words
shadow <number_small> <user.ordinals>:
    user.vim_normal_mode_exterm("{number_small}k")
    key('0')
    insert("{ordinals}W")
    insert("yW")
    insert(":set nohls\n")
    user.vim_set_insert_mode()
    edit.paste()
    key(space)

echo <number_small>:
    user.vim_normal_mode_exterm("{number_small}k")
    key('0')
    insert("yW")
    insert(":set nohls\n")
    user.vim_set_insert_mode()
    edit.paste()
    key(space)
