tag: terminal
and tag: user.git
-
get hub {user.github_command} [<user.github_arguments>]:
    args = github_arguments or ""
    "gh {github_command}{args} "

# Convenience
github repo clone clipboard:
    insert("gh repo clone ")
    edit.paste()
    key(enter)
