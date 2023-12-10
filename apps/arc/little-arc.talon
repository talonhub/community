user.running: arc
-
little arc [<user.text>]:
   key("cmd-alt-n")
    actions.user.switcher_focus_app("arc")
    insert(user.text or "")
