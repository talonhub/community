# https://github.com/gcmt/taboo.vim/
tag: vim
-

tab rename: user.vim_normal_mode_exterm(":TabooRename ")
tab rename <user.text>: user.vim_normal_mode_exterm(":TabooRename {text}")
new tab named: user.vim_normal_mode_exterm(":TabooOpen ")
new tab named <user.text>: user.vim_normal_mode_exterm(":TabooOpen {text}")
tab reset: user.vim_normal_mode_exterm(":TabooReset\n")
