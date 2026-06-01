tag: terminal
and tag: user.git
-
jojo {user.jujitsu_command} [<user.jujitsu_arguments>]:
    args = jujitsu_arguments or ""
    "jj {jujitsu_command}{args} "
jojo describe [<user.jujitsu_arguments>] message [<user.prose>]:
    args = jujitsu_arguments or ""
    message = prose or ""
    user.insert_between('jj describe{args} --message "{message}', '"')
jojo new [<user.jujitsu_arguments>] message [<user.prose>]:
    args = jujitsu_arguments or ""
    message = prose or ""
    user.insert_between('jj new{args} --message "{message}', '"')
jojo commit [<user.jujitsu_arguments>] message [<user.prose>]:
    args = jujitsu_arguments or ""
    message = prose or ""
    user.insert_between('jj commit{args} --message "{message}', '"')

# Optimistic execution for frequently used commands that are harmless (don't
# change repository or index state).
jojo status$: "jj status\n"
jojo show head$: "jj show HEAD\n"
jojo diff head$: "jj diff\n"
