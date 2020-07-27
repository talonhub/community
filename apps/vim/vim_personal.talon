tag: vim
-

###
# Convenience for opening my different files
###
open talon (directory|dir):
    user.vim_command_mode_exterm(":lcd ~/.talon/user/fidget/\n")
edit my vim scripts:
    user.vim_command_mode_exterm(":source ~/.vim/sessions/talon_vim.session\n")

open custom snippets:
    user.vim_command_mode_exterm(":e ~/.vim/custom-snippets\n")
open vim snippets:
    user.vim_command_mode_exterm(":e ~/.vim/plugged/vim-snippets/UltiSnips/\n")
open markdown snippets:
    user.vim_command_mode_exterm(":e ~/.vim/plugged/vim-snippets/UltiSnips/markdown.snippets\n")
open python snippets:
    user.vim_command_mode_exterm(":e ~/.vim/plugged/vim-snippets/UltiSnips/python.snippets\n")
open bash snippets:
    user.vim_command_mode_exterm(":e ~/.vim/plugged/vim-snippets/UltiSnips/sh.snippets\n")

###
#
###
fine merge conflict:
    user.vim_command_mode_exterm(":/\c<<<\n")

dick to class member:
    user.vim_normal_mode("ds[ds\"i.")

###
# Things that mix vim and other command
###
# XXX - rename
super focus:
    # i3wm full screen toggle
    key(super-f)
    # wait for redraw
    sleep(200ms)
    # equalize vim splits
    user.vim_set_normal_mode_exterm()
    key(ctrl-w)
    key(=)

###
# Email writing
###

nest this:
    user.vim_set_normal_mode()
    key(0)
    key(m ')
    insert("gqap")
    key(')
    key(')
    key(0)
    user.vim_set_visual_block_mode()
    key(} up)
    key(0 I > space escape)

tidy nest:
    user.vim_set_normal_mode()
    key(0 l)
    user.vim_set_visual_block_mode()
    key(} up l)
    key(I space escape)

# turn a non line wrapped email response into a more wealth formatted
# traditional style nesting
re nest this:
    key(0)
    user.vim_set_visual_block_mode()
    key(} up)
    key(0 I > escape)
