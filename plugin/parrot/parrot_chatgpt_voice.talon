mode: user.chatgpt_voice
--

parrot(cluck):
    user.switcher_focus("ChatGPT")
    app.window_close()
    mode.disable("user.chatgpt_voice")
    mode.enable("command")
    user.system_command_nb("curl -X 'GET' \"http://10.0.0.151/show?letter=C\"")