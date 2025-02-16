app: microsoft_edge
-
settings():
    user.context_sensitive_dictation = true
    # This is intentionally disabled, as it does not work in the address bar
    # See edge.py's implementation of insert
    user.paste_to_insert_threshold =  0
    
tag(): browser
tag(): user.tabs
