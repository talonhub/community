mode: sleep
-

parrot(cluck): 
    speech.enable()
    app.notify("Woke Up")
    user.system_command_nb("curl -X 'GET' \"http://10.0.0.151/show?letter=C\"")
    