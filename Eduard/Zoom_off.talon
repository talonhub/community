os: windows
and app.name: Zoom Meetings
os: windows
and app.exe: Zoom.exe
mode: sleep
-

^microphone off:
  key('alt-a')
  user.talon_mode()
  user.connect_ocr_eye_tracker()

^switch camera:
  key('alt-v')

  

