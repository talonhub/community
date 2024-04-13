# This file activates talon-specific python commands
# by default, it simply looks for the python tag to be active
# lines 7-11 provide examples to make the activation more specific
# which may be preferred by people who code in other python projects
# app: vscode
# Mac VSCode uses an em-dash
# win.title: /— user/
# win.title: /— community/
# windows VSCode uses an en-dash
# win.title: / - user - Visual Studio Code/
# win.title: / - community - Visual Studio Code/
code.language: python
-
tag(): user.talon_python
