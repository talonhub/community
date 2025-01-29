mode: user.flow
-

parrot (cluck):
    key('fn-space')
    mode.disable("user.flow")
    mode.enable("command")
    user.system_command_nb("curl -X 'GET' \"http://10.0.0.151/show?letter=C\"")
