os: mac
-
^desktop$: user.dock_send_notification("com.apple.showdesktop.awake")
^window$: user.dock_send_notification("com.apple.expose.awake")
^launch pad$: user.dock_send_notification("com.apple.launchpad.toggle")
