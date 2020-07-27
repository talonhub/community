# these commands are based off the official the markdown vim-snippets
tag: vim
code.language: markdown
-

###########################
# Sections and Paragraphs #
###########################
snip section:
    user.vim_insert_mode("sec")
    key(tab)

snip sub section:
    user.vim_insert_mode("ssec")
    key(tab)

snip sub sub section:
    user.vim_insert_mode("sssec")
    key(tab)

snip paragraph:
    user.vim_insert_mode("par")
    key(tab)

snip sub paragraph:
    user.vim_insert_mode("spar")
    key(tab)

###################
# Text formatting #
###################
snip italics:
    user.vim_insert_mode("*")
    key(tab)

snip bold:
    user.vim_insert_mode("**")
    key(tab)

snip bold italics:
    user.vim_insert_mode("***")
    key(tab)

snip comment:
    user.vim_insert_mode("/*")
    key(tab)

################
# Common stuff #
################
snip link:
    user.vim_insert_mode("link")
    key(tab)

snip image:
    user.vim_insert_mode("img")
    key(tab)

snip [in line] code:
    user.vim_insert_mode("ilc")
    key(tab)

snip code block:
    user.vim_insert_mode("cbl")
    key(tab)

snip (ref|reference) link:
    user.vim_insert_mode("refl")
    key(tab)

snip footnote:
    user.vim_insert_mode("fnt")
    key(tab)

snip detail:
    user.vim_insert_mode("detail")
    key(tab)

snip table <number_small> <number_small>:
    user.vim_insert_mode("tb(")
    insert("{number_small_1}{number_small_2})")
    key(tab)
