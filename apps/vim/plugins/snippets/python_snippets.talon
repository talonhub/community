tag: vim
code.language: python
-
###
# Public snippets - part of vim-snippets
###

(snip|snippet) header:
    user.vim_insert_mode("#!")
    key(tab)

(snip|snippet) if main:
    user.vim_insert_mode("ifmain")
    key(tab)

(snip|snippet) for loop:
    user.vim_insert_mode("for")
    key(tab)

(snip|snippet) (dark|dock) string class:
    user.vim_insert_mode("class")
    key(tab)

(snip|snippet) (dark|dock) string function:
    user.vim_insert_mode("def")
    key(tab)

(snip|snippet) (dark|dock) string method$:
    user.vim_insert_mode("defc")
    key(tab)

(snip|snippet) (dark|dock) string static method$:
    user.vim_insert_mode("defs")
    key(tab)

(snip|snippet) from import:
    user.vim_insert_mode("from")
    key(tab)

(snip|snippet) if:
    user.vim_insert_mode("if")
    key(tab)

(snip|snippet) if else$:
    user.vim_insert_mode("ife")
    key(tab)

(snip|snippet) if if else$:
    user.vim_insert_mode("ifee")
    key(tab)

(snip|snippet) try:
    user.vim_insert_mode("try")
    key(tab)

###
# Private snippets
#
# Place your private snippets here that other Talon users won't be able to
# use
###

(snip|snippet) print success:
    user.vim_insert_mode("psuccess")
    key(tab)

(snip|snippet) print fail:
    user.vim_insert_mode("pfail")
    key(tab)

(snip|snippet) dick string:
    user.vim_insert_mode("dstr")
    key(tab)

(snip|snippet) new arg parser:
    user.vim_insert_mode("argparse")
    key(tab)

(snip|snippet) add (arg|argument):
    user.vim_insert_mode("narg")
    key(tab)
