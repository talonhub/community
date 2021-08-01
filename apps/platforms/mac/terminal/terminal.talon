app: apple_terminal
-
#comment or remove tags for command sets you don't want
tag(): user.file_manager
tag(): user.generic_terminal
tag(): user.git
tag(): user.kubectl
tag(): user.tabs
tag(): terminal
rerun search:
    key(ctrl-r)
suspend:
    key(ctrl-z)
resume:
    insert("fg")
    key(enter)

# Required as of August 1 2021 allow terminal copy-paste on Mac with zsh (default terminal)
# https://github.com/knausj85/knausj_talon/issues/521
copy that:
    key(cmd-c)
paste that:
    key(cmd-v)
