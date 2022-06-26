os: mac
-

^cast [<user.text>]$:
  user.raycast(text)

^cast {user.raycast_command}$:
  user.raycast(user.raycast_command)
  key(enter)

^cast {user.raycast_input_command} [<user.text>]$:
  user.raycast(user.raycast_input_command, user.text or "")

^menu [<user.text>]$:
  key(ctrl-alt-space)
  sleep(150ms)
  insert(text or "")

^switch [<user.text>]$:
  key(alt-space)
  sleep(150ms)
  insert(text or "")
