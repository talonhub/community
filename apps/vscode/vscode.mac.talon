app: Code
os: mac

-
# Navigation and commands
run command: key(cmd-shift-p)

action(user.ide_find_file):
    key(cmd-p)

action(user.ide_find_everywhere):
    key(cmd-shift-f)

(search | find) file: user.ide_find_file()
(search | find) (everywhere | all): user.ide_find_everywhere()

# Editing
copy [line] down: key(shift-alt-down)
copy [line] up: key(shift-alt-up)
