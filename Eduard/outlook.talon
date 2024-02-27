os: windows
and app.name: Microsoft Outlook
os: windows
and app.exe: OUTLOOK.EXE
-

send email: key('ctrl+enter')

insert: 
    key('alt')
    sleep(300ms)
    key('n')
    sleep(1500ms)
    key('a')
    key('f')

settings():
    user.context_sensitive_dictation = 0


