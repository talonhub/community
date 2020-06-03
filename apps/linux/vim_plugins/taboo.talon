# https://github.com/gcmt/taboo.vim/
tag: vim
-

tab rename: user.vim_normal_mode(":TabooRename ")
tab rename <user.text>: user.vim_normal_mode(":TabooRename {text}")
new tab named: user.vim_normal_mode(":TabooOpen ")
new tab named <user.text>: user.vim_normal_mode(":TabooOpen {text}")
tab reset: user.vim_normal_mode(":TabooReset\n")
