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

lisa: insert("ls\n")

file list: "ls "
file link: "ln -s "
file move: "mv "
file copy: "cp "
file type: "file
file show: "cat "
file stat: "stat " 

# directories

get link:
    insert("readlink -f ")
# directory and files
pivot: "cd "
pivot clip:
    insert("cd ")
    edit.paste()
    key(enter)
pivot <user.paths>:
    insert("cd {paths}\n")
    insert("ls\n")
# pivot up doesn't work with talon
(go parent|pivot back): "cd ../\n"
pivot <number_small> back: 
    insert("cd ")
    insert(user.path_traverse(number_small))
    key(enter)
folder (create|new): "mkdir -p  "
(go home|pivot home): "cd\n"
go projects: "cd ~/projects\nls\n"
# grepping

rip: "rg -i "
rip around: "rg -B2 -A2 -i "
rip (exact|precise): "rg "
now rip:
    edit.up()
    insert("| rg -i ")

make executable: "chmod +x "
run top: "htop\n"
run vim: "vim "
run code: "code "

current folder copy: "pwd | tr -d \\\\n\\\\r | pbcopy\n"
current folder: "pwd\n"

# brew
brew install: insert("brew install ")
brew search: insert("brew search ")
brew info: insert("brew info ")

# dotfiles
dotfiles add: insert("yadm add ")
dotfiles status: insert("yadm status\n")
dotfiles sync: 
    insert("yadm add -u\n")
    insert("yadm commit -m 'Changes'\n")
    insert("yadm push -u origin master\n")

copy paste:
    edit.copy()
    edit.paste()
