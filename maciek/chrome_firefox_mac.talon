os: mac
app: firefox
app: chrome
-
show links: key("f")
link: key("f")
new link: key(shift-f)

go search [<user.text>]$: 
    key("o")
    sleep(200ms)
    insert(text or "")
    
go search that: 
    key("o")
    sleep(200ms)
    key(cmd-v)

copy link: key(y f)
copy (address | url): 
    key(escape y y)
    sleep(100ms)

close: 
    app.tab_close()
    sleep(40ms)
go front: browser.go_forward()
next: app.tab_next()
last: app.tab_previous()
back: browser.go_back()
front: browser.go_forward()

go find [<user.text>]$: 
    key(cmd-f)
    sleep(200ms)
    insert(text or "")
    # user.text_field_mode(phrase or "")

find this:
    key(cmd-c)
    key(cmd-f)
    sleep(200ms)
    key(cmd-v)
