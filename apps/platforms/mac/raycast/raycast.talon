os: mac
-

# todo: talon doesn't seem able to detect when raycast is focused

^cast [<user.text>]$:
  user.raycast(text or "")

^cast {user.raycast_command}$:
  user.raycast(user.raycast_command)
  key(enter)

^cast {user.raycast_input_command} [<user.text>]$:
  user.raycast(user.raycast_input_command, user.text or "")

^menu [<user.text>]$:
  key(ctrl-alt-space)
  sleep(150ms)
  insert(text or "")

^switch [<user.running_applications>]$:
  key(alt-space)
  sleep(150ms)
  insert(user.running_applications or "")

^cast go <number_small>$:
  key("cmd-{number_small}")
