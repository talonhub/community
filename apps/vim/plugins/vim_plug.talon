tag: vim
-

plugins install:
    user.vim_normal_mode_exterm(":so $MYVIMRC\n")
    user.vim_normal_mode_exterm(":PlugInstall\n")
plugins status:
    user.vim_normal_mode_exterm(":so $MYVIMRC\n")
    user.vim_normal_mode_exterm(":PlugStatus\n")
plugins clean:
    user.vim_normal_mode_exterm(":so $MYVIMRC\n")
    user.vim_normal_mode_exterm(":PlugClean\n")
plugins diff:
    user.vim_normal_mode_exterm(":so $MYVIMRC\n")
    user.vim_normal_mode_exterm(":PlugDiff\n")
plugins update:
    user.vim_normal_mode_exterm(":so $MYVIMRC\n")
    user.vim_normal_mode_exterm(":PlugUpdate\n")
plugins upgrade:
    user.vim_normal_mode_exterm(":so $MYVIMRC\n")
    user.vim_normal_mode_exterm(":PlugUpgrade\n")
plugins snapshot:
    user.vim_normal_mode_exterm(":so $MYVIMRC\n")
    user.vim_normal_mode_exterm(":PlugSnapshot\n")
