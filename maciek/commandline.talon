os:mac
mode: user.terminal
mode: command
and tag: terminal
-
# There are two modes and one tag, do I really need this because I'm a little confused?

# file list: "ls "
# file list here: "ls\n"
# file list long: "ls -al "
# file list long here: "ls -al\n"
file list latest: "ls -Art | tail -n1\n"
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
# here: "./"
python: "python "
in home: insert(" ~/")
describe: insert("tldr ")
talon play latest: insert("talon-play-latest\n")

lisa: insert("ls\n")
    
###############################################################################
### file operations
###############################################################################
file list: "ls "
file link: "ln -s "
file move: "mv "
file copy: "cp "
dir copy: "cp -r "
file type: "file "
file show: "cat "
file stat: "stat " 
file which: "which "
get link: insert("readlink -f ")


###############################################################################
### directory navigation
###############################################################################
  
pivot that:
    insert("cd ")
    edit.paste()
    key(enter)
pivot <user.paths>:
    insert("cd {paths}\n")
    insert("ls\n")
# pivot up doesn't work with talon
go parent: "cd ../\n"
pivot <number_small> back: 
    insert("cd ")
    insert(user.path_traverse(number_small))
    key(enter)

make dir: "mkdir -p  
go home: "cd\n"
folder path copy : insert("pwd | tr -d \\\\n\\\\r | pbcopy\n")
clipboard that:
    key(up end)
    " | tr -d \\\\n\\\\r | pbcopy\n"


###############################################################################
### projects directory
###############################################################################
projects go: 
    insert("cd ~/projects\n")
    user.fzf_cd_directory_single_level()

projects jump: insert("cd ~/projects\n")
force remove: "rm -rf "
# grepping

rip around: "rg -B2 -A2 -i "
rip: "rg -i "
rip (exact|precise): "rg "
now rip that:
    edit.up()
    insert("| rg -i ")


make executable: "chmod +x "

top run: "top\n"
vim run: "vim "
code run: "code "

current folder: "pwd\n"

fish reload: 
    insert("fish-config-reload\n")
fish config:
    insert("fish-config\n")
s q lite browser:
    insert("sqlite-browser ")

###############################################################################
### dotfiles
###############################################################################
dotfiles add: insert("yadm add ")
dotfiles status: insert("yadm status\n")
dotfiles sync: 
    insert("yadm add -u\n")
    insert("yadm commit -m 'Changes'\n")
    insert("yadm push -u origin master\n")

# npm stuff
npm test: 
    insert("npm run test\n")
copy paste:
    edit.copy()
    edit.paste()

talon repl:insert("talon-repl\n")     

which [<user.text>]:
    insert("which ")
    insert(text or "")

cube nine: insert("k9s\n")
# cluster control:
#     insert("k0sctrl ")    

vars show: "env\n"
# Taskfile
task: insert("task \t")

# vd command
# vidi: insert("vd ") 
###############################################################################
### ssh stuff
###############################################################################
remote shell: insert("ssh ")
pink google: insert("ping www.google.com\n")
pink google d n s: "ping 8.8.8.8\n"
    
remote shell tesla:
    insert("ssh tesla.maciejk.dev\n")
    sleep(1000ms)
    insert("fish\n")
remote shell pie|raspberry:
    insert("ssh raspberry.maciejk.dev\n")
    sleep(1000ms)
    # insert("fish\n")
    
shell logout: insert("exit\n")


# this is for broot
rsync: insert("rsync -avz ")
brick: insert("br -h\n")
brick home: insert("br -h ~/\n")
brick root: insert("br -h /\n")
    

git ui: "gitui\n"

oxy: insert("zi\n")

gitignore: insert(".gitignore ") 
sudo: insert("sudo ")
unzip: insert("unzip ")
z f s: insert("zfs \t")
z pool: insert("zpool \t")
add sudo: 
    key(home)
    insert("sudo ")
add help: insert(" --help ")
pager: " | less "
run last:
    key(up)
    key(enter)
manual: "man "
(take it|accept):
    key(right)
    key(enter)

navi: insert("navi\n")
command copy:key(cmd-alt-shift-c)
lazy docker: "lazydocker\n"
sudo reboot: "sudo reboot"
run it:
    edit.paste()
    key(enter)


pip|peep:insert("python -m pip ")
(pip|peep) freeze: insert("python -m pip freeze\n")
(pip|peep) install: insert("python -m pip install ")

virtual env: insert("python -m venv ")
virtual activate: insert("source .venv/bin/activate")
virtual activate fish: insert("source .venv/bin/activate.fish")

tar decompress: insert("tar -xvf ")

g util: insert("gsutil ")
g util copy: insert("gsutil cp ")
g util move: insert("gsutil mv ")

list: insert("ls ")