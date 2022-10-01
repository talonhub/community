# NOTE: to use these commands you will need to activate the tag below in whatever contexts you
# choose.
#
# do this in a separate .talon file or via python. for example, if you use windows terminal for
# wsl then you might do this:
#
#    os: windows
#    app: windows_terminal
#    -
#    tag(): user.wsl
#
# however, if you also use windows terminal for other things (powershell), you will want something
# more specific...like this:
#
#    os: windows
#    app: windows_terminal
#    title: /^WSL:/
#    -
#    tag(): user.wsl
#
# then, you will need to find a way to set the window title accordingly. for example, to match
# the title pattern above, you can set the prompt in your .bashrc file like this:
#
#    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}WSL:${WSL_DISTRO_NAME} \u@\h: \w\a\]$PS1"
#
# ALSO: if you do populate your window title with your distro name, make sure the 'wsl_title_regex'
# value in wsl.py is set accordingly.
tag: user.wsl
-

tag(): terminal
tag(): user.file_manager
tag(): user.generic_unix_shell
tag(): user.git
tag(): user.kubectl

^go <user.letter>$: user.file_manager_open_volume("/mnt/{letter}")

(wsl | weasel) reset path detection: user.wsl_reset_path_detection()
(wsl | weasel) speak: user.wsl_speak()
