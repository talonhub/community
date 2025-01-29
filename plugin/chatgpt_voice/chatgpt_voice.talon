^voice chat:
    mode.disable("command")
    mode.disable("dictation")
    mode.enable("user.chatgpt_voice")
    user.system_command("shortcuts run chatgpt")
    user.system_command_nb("curl -X 'GET' \"http://10.0.0.151/show?letter=V\"")
