tag: vim
-

plugins install:
    user.vim_normal_mode(":so $MYVIMRC\n")
    user.vim_normal_mode(":PlugInstall\n")
plugins status:
    user.vim_normal_mode(":so $MYVIMRC\n")
    user.vim_normal_mode(":PlugStatus\n")
plugins clean:
    user.vim_normal_mode(":so $MYVIMRC\n")
    user.vim_normal_mode(":PlugClean\n")
plugins diff:
    user.vim_normal_mode(":so $MYVIMRC\n")
    user.vim_normal_mode(":PlugDiff\n")
plugins update:
    user.vim_normal_mode(":so $MYVIMRC\n")
    user.vim_normal_mode(":PlugUpdate\n")
plugins upgrade:
    user.vim_normal_mode(":so $MYVIMRC\n")
    user.vim_normal_mode(":PlugUpgrade\n")
plugins snapshot:
    user.vim_normal_mode(":so $MYVIMRC\n")
    user.vim_normal_mode(":PlugSnapshot\n")
