user.running: fluentsearch
-
gpt [<user.text>]: 
    txt = text or ""
    user.system_search()
    sleep(100ms)
    user.paste("chatgpt: {txt}")