os: windows
and app.name: Zoom Meetings
os: windows
and app.exe: Zoom.exe
mode: command
-

^microphone on:
  key('alt-a')
  user.switcher_hide_running()
  user.history_disable()
  user.homophones_hide()
  user.help_hide()
  user.mouse_sleep()
  user.disconnect_ocr_eye_tracker()
  speech.disable()
  user.engine_sleep()

^switch camera:
  key('alt-v')

  

