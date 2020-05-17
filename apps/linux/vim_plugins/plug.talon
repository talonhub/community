os: linux
tag: vim
-

plugins install:
    insert(":so $MYVIMRC\n")
    insert(":PlugInstall\n")
plugins status:
    insert(":so $MYVIMRC\n")
    insert(":PlugStatus\n")
plugins clean:
    insert(":so $MYVIMRC\n")
    insert(":PlugClean\n")
plugins diff:
    insert(":so $MYVIMRC\n")
    insert(":PlugDiff\n")
plugins update:
    insert(":so $MYVIMRC\n")
    insert(":PlugUpdate\n")
plugins upgrade:
    insert(":so $MYVIMRC\n")
    insert(":PlugUpgrade\n")
plugins snapshot:
    insert(":so $MYVIMRC\n")
    insert(":PlugSnapshot\n")
