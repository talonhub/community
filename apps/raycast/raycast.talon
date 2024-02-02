os: mac
-

# todo: talon doesn't seem able to detect when raycast is focused

^cast [<user.text>]$: user.raycast(text or "")

^cast {user.raycast_command}$:
    user.raycast(raycast_command)
    key(enter)

^cast {user.raycast_input_command} [<user.text>]$:
    user.raycast(raycast_input_command, text or "")

^menu [<user.text>]$:
    key(ctrl-alt-space)
    sleep(150ms)
    insert(text or "")

^switch <user.running_applications>$: user.raycast_switcher(running_applications, true)

^switch$: key(alt-space)

^cast go <number_small>$: key("cmd-{number_small}")

^cast action [<user.text>]$:
    key(cmd-k)
    insert(text or "")
