os:mac
mode: user.terminal
mode: command
and tag: terminal
-
# file list: "ls "
# file list here: "ls\n"
# file list long: "ls -al "
# file list long here: "ls -al\n"
# file list latest: "ls -Art | tail -n1\n"
# file list folders: "ls -d */\n"

# find command
# file find all links: "find . -maxdepth 1 -type l  -ls\n"
# file find all folders: "find . -maxdepth 1 -type d  -ls\n"
# file fine all files: "find . -maxdepth 1 -type f  -ls\n"

# TODO - revisit the grammar for $() commands
# call list latest: "$(ls -Art | tail -n1)"

# TODO - somehow make this scriptable to print anything
# file edit latest: "edit $(ls -Art | tail -n1)\n"
# file latest: "$(ls -Art | tail -n1)"

# added by maciek

parent: "../"
here: "./"
python: "python "
in home: insert(" ~/")
describe: insert("tldr ")
talon play latest: insert("talon-play-latest\n")

lisa: insert("ls ")

file link: "ln -s "
file move: "mv "
file copy: "cp "
file type: "file
file show: "cat "
file stat: "stat " 

(go home|pivot home): "cd\n"
# grepping

rip: "rg -i "
rip around: "rg -B2 -A2 -i "
rip (exact|precise): "rg "
now rip:
    edit.up()
    insert("| rg -i ")

run top: "htop\n"
run vim: "vim "

folder yank: "pwd | tr -d \\\\n\\\\r | pbcopy\n"

# brew
brew install: insert("brew install ")
brew search: insert("brew search ")
brew info: insert("brew info ")
